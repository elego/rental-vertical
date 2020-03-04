from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    #start_datetime = fields.Datetime(string="Start Date")
    #end_datetime = fields.Datetime(string="End Date")

    #TODO add new rental_type 'rental_forword' to bypass the product from a customer to another customer
    # new Many2one fields forword_rental_id
    # onchange_forword_rental_id -> set planned_source_address_id and planned_in_location_id
    # by confirmation of the rental order create wizard sale.rental.route automatically


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
        # After spliting the in_move of the rental we can not use it 
        # as rental_extension or sell_rental anymore
        for line in self:
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
                    if move.picking_type_id.code == 'outgoing':
                        res["out_move_id_bk"] = move.id
                        move.write({"move_dest_ids": [(5, 0, 0)]})
                    elif move.picking_type_id.code == 'incoming':
                        res["in_move_id_bk"] = move.id
                        move.state = "confirmed"
                    else:
                        move.write({"move_dest_ids": [(5, 0, 0)]})
                        move.state = "confirmed"
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

    #(override)
    def _run_rental_procurement(self, line, vals):
        location = line.order_id.warehouse_id.rental_out_location_id
        if line.order_id.partner_shipping_id.rental_onsite_location_id:
            location = line.order_id.partner_shipping_id.rental_onsite_location_id
        self.env['procurement.group'].run(
            line.product_id.rented_product_id, line.rental_qty,
            line.product_id.rented_product_id.uom_id,
            location,
            line.name, line.order_id.name, vals)

    @api.multi
    def _prepare_new_rental_procurement_values(self, group=False):
        res = super(SaleOrderLine, self)._prepare_new_rental_procurement_values(group=group)
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


