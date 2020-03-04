from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    start_datetime = fields.Datetime(string="Start Date")
    end_datetime = fields.Datetime(string="End Date")

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
        for line in self:
            if line.rental_type == "rental_extension":
                if not line.extension_rental_id:
                    raise ValidationError(
                        _(
                            "Missing 'Rental to Extend' on the sale order line "
                            "with rental service %s"
                        )
                        % line.product_id.name
                    )
                if line.rental_qty != line.extension_rental_id.rental_qty:
                    raise ValidationError(
                        _(
                            "On the sale order line with rental service %s, "
                            "you are trying to extend a rental with a rental "
                            "quantity (%s) that is different from the quantity "
                            "of the original rental (%s). This is not supported."
                        )
                        % (
                            line.product_id.name,
                            line.rental_qty,
                            line.extension_rental_id.rental_qty,
                        )
                    )
            if line.rental_type in ("new_rental", "rental_extension"):
                if not line.product_id.rented_product_id:
                    raise ValidationError(
                        _(
                            "On the 'new rental' sale order line with product "
                            "'%s', we should have a rental service product !"
                        )
                        % (line.product_id.name)
                    )
            elif line.sell_rental_id:
                if line.product_uom_qty != line.sell_rental_id.rental_qty:
                    raise ValidationError(
                        _(
                            "On the sale order line with product %s "
                            "you are trying to sell a rented product with a "
                            "quantity (%s) that is different from the rented "
                            "quantity (%s). This is not supported."
                        )
                        % (
                            line.product_id.name,
                            line.product_uom_qty,
                            line.sell_rental_id.rental_qty,
                        )
                    )

    @api.multi
    def prepare_rental_values(self, group_id=False):
        res = super(SaleOrderLine, self).prepare_rental_values(group_id=group_id)
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
            onsite_location = self.order_id.partner_shipping_id.rental_onsite_location_id
            if onsite_location:
                res.update({'onsite_location_id': onsite_location.id})
        return res

    @api.multi
    def _prepare_rental(self):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_rental()
        if res:
            if self.move_ids:
                for move in self.move_ids:
                    if move.move_dest_ids:
                        res["out_move_id_bk"] = move.id
                        res["in_move_id_bk"] = move.move_dest_ids[0].id
                        move.move_dest_ids[0].state = "confirmed"
                        move.write({"move_dest_ids": [(5, 0, 0)]})
            if self.order_id.partner_shipping_id.rental_onsite_location_id:
                res[
                    "rental_onsite_location_id"
                ] = (
                    self.order_id.partner_shipping_id.rental_onsite_location_id.id
                )
            else:
                res[
                    "rental_onsite_location_id"
                ] = self.order_id.warehouse_id.rental_out_location_id.id
        return res
