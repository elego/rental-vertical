# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare
from odoo.osv import expression

class SaleOrder(models.Model):
    _inherit = "sale.order"

    rental_stock_product_line_ids = fields.One2many(
        "rental.stock.product.line",
        "order_id",
        string="Product Lines",
    )

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        res = super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
        args = args or []
        rental_routing = self.env.context.get("rental_routing", False)
        if rental_routing:
            start_date = fields.Date.from_string(self.env.context.get("start_date", False))
            rental_order_id = self.env.context.get("rental_order_id", False)
            domain = [
                "&",
                ("id", "!=", rental_order_id),
                ("state", "=", "sale"),
            ]
            record_ids = self._search(
                expression.AND([domain, args]),
                limit=limit,
                access_rights_uid=name_get_uid,
            )
            if record_ids:
                res2 = self.browse(record_ids).filtered(lambda x: x.default_end_date and x.default_end_date < start_date).name_get()
                return list(set(res) & set(res2))
        return res

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            out_pickings = order.picking_ids.filtered(
                lambda x: x.picking_type_id.code == "outgoing" and x.state != "cancel"
            )
            in_pickings = order.picking_ids.filtered(
                lambda x: x.picking_type_id.code == "incoming" and x.state != "cancel"
            )
            for picking in out_pickings:
                for move in picking.move_ids_without_package:
                    if move.move_dest_ids:
                        move.write({"move_dest_ids": [(5, 0, 0)]})
                    if move.state != "cancel":
                        move.state = "confirmed"
            for picking in in_pickings:
                for move in picking.move_ids_without_package:
                    if move.state != "cancel":
                        move.state = "confirmed"
            order.create_rental_stock_product_line(out_pickings, in_pickings)
        return res

    @api.multi
    def create_rental_stock_product_line(self, out_pickings, in_pickings):
        self.ensure_one()
        rspl_obj = self.env["rental.stock.product.line"]
        line_dict = {}
        for picking in out_pickings:
            for move in picking.move_ids_without_package:
                if move.product_id.pack_ok \
                        or move.location_id != self.warehouse_id.rental_in_location_id:
                    continue
                if move.product_id.id not in line_dict:
                    line_dict[move.product_id.id] = {
                        "order_id": self.id,
                        "product_id": move.product_id.id,
                        "product_qty_out": move.product_qty,
                        "product_qty_in": 0,
                        "out_move_ids": [(4, move.id, 0)],
                        "out_move_id": move.id,
                        "in_move_ids": [],
                    }
        for picking in in_pickings:
            for move in picking.move_ids_without_package:
                if move.product_id.pack_ok \
                        or move.location_dest_id != self.warehouse_id.rental_in_location_id:
                    continue
                if move.product_id.id in line_dict:
                    line_dict[move.product_id.id]["in_move_ids"].append((4, move.id, 0))
                    line_dict[move.product_id.id]["in_move_id"] = move.id
                    line_dict[move.product_id.id]["product_qty_in"] += move.product_qty
        for key, val in line_dict.items():
            new_line = rspl_obj.create(val)


class RentalStockProductLine(models.Model):
    _name="rental.stock.product.line"

    order_id = fields.Many2one(
        comodel_name="sale.order",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    out_move_ids = fields.Many2many(
        comodel_name="stock.move",
        relation="out_move_rental_product_line_rel",
        column1="move_id",
        column2="line_id",
        string="Moves (Inbound)",
    )
    in_move_ids = fields.Many2many(
        comodel_name="stock.move",
        relation="in_move_rental_product_line_rel",
        column1="move_id",
        column2="line_id",
        string="Moves (Outbound)",
    )
    out_move_id = fields.Many2one(
        comodel_name="stock.move",
        string="Origin Move (Inbound)",
    )
    in_move_id = fields.Many2one(
        comodel_name="stock.move",
        string="Origin Moves (Outbound)",
    )
    product_qty_out = fields.Float(
        string="Initial Demand",
    )
    product_qty_in = fields.Float(
        string="Initial Demand (Outbound)",
        help="Technical Field, Value of this field should always equal to product_qty_out"
    )
    routed_qty_out = fields.Float(
        string="Routed (Inbound)",
    )
    routed_qty_in = fields.Float(
        string="Routed (Outbound)",
    )
    reduced_qty_out = fields.Float(
        string="Reduced (Inbound)",
    )
    reduced_qty_in = fields.Float(
        string="Reduced (Outbound)",
    )
    total_qty_out = fields.Float(
        string="Total (Inbound)",
        compute="_compute_total_qty",
    )
    total_qty_in = fields.Float(
        string="Total (Outbound)",
        compute="_compute_total_qty",
    )

    @api.multi
    def _compute_total_qty(self):
        for rec in self:
            total_qty_out = 0
            total_qty_in = 0
            for move in rec.out_move_ids:
                if move.state != "cancel":
                    total_qty_out += move.product_qty
            for move in rec.in_move_ids:
                if move.state != "cancel":
                    total_qty_in += move.product_qty
            rec.total_qty_out = total_qty_out
            rec.total_qty_in = total_qty_in

    @api.multi
    def _get_routed_qty(self, rental_type):
        routed_qty = 0
        if rental_type == 'out':
            for move in self.out_move_ids:
                if move.location_id == self.order_id.warehouse_id.rental_in_location_id \
                        or move.state == "cancel":
                    continue
                routed_qty += move.product_qty
        if rental_type == 'in':
            for move in self.in_move_ids:
                if move.location_dest_id == self.order_id.warehouse_id.rental_in_location_id \
                        or move.state == "cancel":
                    continue
                routed_qty += move.product_qty
        return routed_qty

    @api.multi
    def _get_origin_rental_moves(self, route_type):
        self.ensure_one()
        res = self.env["stock.move"]
        rental_in = self.order_id.warehouse_id.rental_in_location_id
        if route_type == "out":
            return self.out_move_ids.filtered(
                lambda x: x.location_id == rental_in and x.state not in ("cancel", "done")
            )
        elif route_type == "in":
            return self.in_move_ids.filtered(
                lambda x: x.location_dest_id == rental_in and x.state not in ("cancel", "done")
            )
        else:
            return res

    @api.multi
    def forward_product(self, forward_line, qty, new_picking):
        self.ensure_one()
        if forward_line.product_id == self.product_id:
            rounding = self.product_id.uom_id.rounding
            in_move = forward_line.in_move_id
            out_move = self.out_move_id
            if not in_move or not out_move:
                raise exceptions.UserError(_("No found origin rental moves."))
            location = in_move.location_id
            location_dest = out_move.location_dest_id

            #split moves in in_moves of forward_line and assign the new_move to the given new picking
            reset_qty = False
            if (
                float_compare(
                    in_move.product_qty,
                    qty,
                    precision_rounding=rounding,
                )
                == 0
            ):
                in_move.product_uom_qty += 1
                reset_qty = True
            new_move_id = in_move.with_context(do_not_push_apply=True)._split(qty)
            if reset_qty:
                in_move.product_uom_qty -= 1
            new_move = self.env["stock.move"].browse(new_move_id)
            new_move.write(
                {
                    "location_id": location.id,
                    "location_dest_id": location_dest.id,
                    "group_id": out_move.group_id.id,
                    "picking_id": new_picking.id,
                    "rental_out_line_id": self.id,
                    "rental_in_line_id": forward_line.id,
                    "origin": "%s -> %s" %(forward_line.order_id.name, self.order_id.name),
                }
            )
            #update referenced moves for current line and forward line
            self.write({"out_move_ids": [(4, new_move.id, 0)]})
            forward_line.write({"in_move_ids": [(4, new_move.id, 0)]})
            #update reduced_qty_in and routed_qty in forward line
            forward_line.reduced_qty_in += qty
            forward_line.routed_qty_in = forward_line._get_routed_qty("in")
            # Quantity that we send to the customer, which is not rented for the current rental order.
            increase_qty = qty
            #update reduced_qty_out and routed_qty in current line
            if (
                float_compare(
                    self.product_qty_out,
                    self.routed_qty_out,
                    precision_rounding=rounding,
                )
                > 0
            ):
                to_be_reduced_qty = qty
                increase_qty = 0
                if (
                    float_compare(
                        qty,
                        self.product_qty_out - self.routed_qty_out,
                        precision_rounding=rounding,
                    )
                    > 0
                ):
                    to_be_reduced_qty = self.product_qty_out - self.routed_qty_out
                    increase_qty = qty - to_be_reduced_qty
                self.reduced_qty_out += to_be_reduced_qty
                if (
                    float_compare(
                        out_move.product_uom_qty,
                        to_be_reduced_qty,
                        precision_rounding=rounding,
                    )
                    > 0
                ):
                    out_move.product_uom_qty -= to_be_reduced_qty
                else:
                    out_move.product_uom_qty = 0
            #Because of the forwarding of products. We send more products as expected.
            #So we have to increase qty of move for (rental in) in current line
            if (
                float_compare(
                    increase_qty,
                    0,
                    precision_rounding=rounding,
                )
                > 0
            ):
                self.in_move_id.product_uom_qty += increase_qty
            self.routed_qty_out = self._get_routed_qty("out")
