from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # onchange_forword_rental_id -> set planned_source_address_id and planned_in_location_id
    # by confirmation of the rental order create wizard sale.rental.route automatically
    can_forward_rental = fields.Boolean("Forward for Rental")
    forward_rental_id = fields.Many2one("sale.rental", string="Rental to Forward")

    @api.constrains(
        "rental_type",
        "extension_rental_id",
        "start_date",
        "end_date",
        "rental_qty",
        "product_uom_qty",
        "product_id",
    )
    def _check_sale_line_rental(self):
        res = super(SaleOrderLine, self)._check_sale_line_rental()
        for line in self:
            # check qty before forwarding rented product form other customer
            if line.rental_type == "new_rental" and line.can_forward_rental:
                if line.forward_rental_id.in_move_id.product_qty < line.rental_qty:
                    raise ValidationError(
                        _(
                            "'Rental to Forward' on the sale order line "
                            "with rental service %s is impossible. You need %s %s."
                            "But only %s %s can be forwarded."
                        )
                        % (
                            line.product_id.name,
                            line.rental_qty,
                            line.product_id.rented_product_id.uom_id.name,
                            line.forward_rental_id.in_move_id.product_qty,
                            line.product_id.rented_product_id.uom_id.name,
                        )
                    )
            # After spliting the in_move of the rental we can not use it
            # as rental_extension or sell_rental anymore
            if line.rental_type == "rental_extension":
                if len(line.extension_rental_id.in_move_ids) > 1:
                    raise ValidationError(
                        _(
                            "'Rental to Extend' on the sale order line "
                            "with rental service %s is impossible. Because"
                            "it is already assigned to other Rental Order."
                        )
                        % line.product_id.name
                    )
            if line.sell_rental_id:
                if len(line.sell_rental_id.in_move_ids) > 1:
                    raise ValidationError(
                        _(
                            "On the sale order line with product %s "
                            "you are trying to sell a rented product, that "
                            "is already assigned to other Rental Order. "
                        )
                        % line.product_id.name
                    )

    @api.multi
    def _prepare_rental(self):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_rental()
        if res:
            if self.move_ids:
                for move in self.move_ids:
                    if move.picking_type_id.code == "outgoing":
                        res["out_move_id_bk"] = move.id
                        move.write({"move_dest_ids": [(5, 0, 0)]})
                    elif move.picking_type_id.code == "incoming":
                        res["in_move_id_bk"] = move.id
                        if move.state != "cancel":
                            move.state = "confirmed"
                    else:
                        move.write({"move_dest_ids": [(5, 0, 0)]})
                        if move.state != "cancel":
                            move.state = "confirmed"
            if self.order_id.partner_shipping_id.rental_onsite_location_id:
                res[
                    "rental_onsite_location_id"
                ] = self.order_id.partner_shipping_id.rental_onsite_location_id.id
            else:
                res[
                    "rental_onsite_location_id"
                ] = self.order_id.warehouse_id.rental_out_location_id.id
        return res

    # (override)
    @api.multi
    def _run_rental_procurement(self, vals):
        self.ensure_one()
        location = self.order_id.warehouse_id.rental_out_location_id
        if self.order_id.partner_shipping_id.rental_onsite_location_id:
            location = self.order_id.partner_shipping_id.rental_onsite_location_id
        self.env["procurement.group"].run(
            self.product_id.rented_product_id,
            self.rental_qty,
            self.product_id.rented_product_id.uom_id,
            location,
            self.name,
            self.order_id.name,
            vals,
        )

    @api.multi
    def _prepare_new_rental_procurement_values(self, group=False):
        res = super(SaleOrderLine, self)._prepare_new_rental_procurement_values(
            group=group
        )
        # RESET route_ids
        if (
            self.product_id.rented_product_id
            and self.order_id.partner_shipping_id.rental_onsite_location_route
        ):
            onside_location_route = (
                self.order_id.partner_shipping_id.rental_onsite_location_route
            )
            if onside_location_route:
                res.update({"route_ids": onside_location_route})
            onsite_location = (
                self.order_id.partner_shipping_id.rental_onsite_location_id
            )
            if onsite_location:
                res.update({"onsite_location_id": onsite_location.id})
        return res

    @api.multi
    def _reset_forward_rental_source(self):
        self.ensure_one()
        if self.can_forward_rental and self.forward_rental_id:
            route_obj = self.env["sale.rental.route"].with_context(
                active_id=self.id, active_model="sale.order.line"
            )
            vals = route_obj.default_get([])
            wizard = route_obj.create(vals)
            out_line = wizard.out_lines[0]
            out_line.rental_in_id = self.forward_rental_id
            out_line.onchange_rental_in_id()
            wizard.action_confirm()
