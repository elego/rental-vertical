from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # onchange_forword_rental_id -> set planned_source_address_id and planned_in_location_id
    # by confirmation of the rental order create wizard sale.rental.route automatically
    can_forward_rental = fields.Boolean(
        string="Route from order",
        help="If set, the product's delivery is not planned "
        "from your own warehouse location but from an "
        "previous order and its used location.",
    )
    forward_rental_id = fields.Many2one(
        comodel_name="sale.rental",
        string="Source",
        help="Please choose a previous order whose delivery "
        "address is now used as the start address for "
        "this new order.",
    )

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
        super(SaleOrderLine, self)._check_sale_line_rental()
        for line in self:
            # check qty before forwarding rented product from other customer
            if line.rental_type == "new_rental" and line.can_forward_rental:
                if line.forward_rental_id.in_move_id.product_qty < line.rental_qty:
                    raise ValidationError(
                        _(
                            "'Route from order' on the sale order line "
                            "with rental service %s is impossible. You need %s %s. "
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
            # After splitting the in_move of the rental we can not use it
            # as rental_extension or sell_rental anymore
            if line.rental_type == "rental_extension":
                if len(line.extension_rental_id.in_move_ids) > 1:
                    raise ValidationError(
                        _(
                            "'Rental to Extend' on the sale order line "
                            "with rental service %s is impossible because "
                            "it is already assigned to another rental order."
                        )
                        % line.product_id.name
                    )
            if line.sell_rental_id:
                if len(line.sell_rental_id.in_move_ids) > 1:
                    raise ValidationError(
                        _(
                            "On the sale order line with product %s "
                            "you are trying to sell a rented product, that "
                            "is already assigned to another rental order. "
                        )
                        % line.product_id.name
                    )

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
                            # move holds 'make_to_order' in v14(compare to v12) so need to change
                            move.procure_method = "make_to_stock"
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
    def _run_rental_procurement(self, vals):
        self.ensure_one()
        location = self.order_id.warehouse_id.rental_out_location_id
        if self.order_id.partner_shipping_id.rental_onsite_location_id:
            location = self.order_id.partner_shipping_id.rental_onsite_location_id
        procurements = [
            self.env["procurement.group"].Procurement(
                self.product_id.rented_product_id,
                self.rental_qty,
                self.product_id.rented_product_id.uom_id,
                location,
                self.name,
                self.order_id.name,
                self.order_id.company_id,
                vals,
            )
        ]
        self.env["procurement.group"].run(procurements)

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

    @api.onchange("can_forward_rental", "start_date", "rental_qty", "product_id")
    def onchange_forward_rental(self):
        if self.rental and self.start_date and self.rental_qty and self.product_id:
            sols = self.search([("forward_rental_id", "!=", False)])
            forwarded_rental_ids = sols.mapped("forward_rental_id").ids
            domain = [
                (
                    "rented_product_id",
                    "=",
                    self.product_id.rented_product_id.id,
                ),
                ("rental_qty", "=", self.rental_qty),
                ("end_date", "<", self.start_date),
                ("id", "not in", forwarded_rental_ids),
                ("state", "!=", "cancel"),
            ]

            return {"domain": {"forward_rental_id": domain}}
        else:
            self.forward_rental_id = False
            return {"domain": {"forward_rental_id": [("id", "=", False)]}}
