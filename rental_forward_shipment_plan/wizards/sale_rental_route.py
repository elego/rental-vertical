# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class SaleRentalRouteOutLine(models.TransientModel):
    _inherit = "sale.rental.route.out.line"

    # (override)
    @api.multi
    def _split_rental_move(self):
        new_move = super()._split_rental_move()
        # (Extension) Create Forward Shipment Plan
        if self.rental_in_move_id.shipment_plan_id and self.move_id.shipment_plan_id:
            order_lines = self.env["sale.order.line"].browse()
            order_lines |= self.rental_id.start_order_line_id
            order_lines |= self.rental_in_id.start_order_line_id
            fsp_vals = self.env["shipment.plan"]._prepare_forward_shipment_plan_values(
                self.rental_in_move_id.shipment_plan_id, self.move_id.shipment_plan_id
            )
            forward_shipment_plan = self.env["shipment.plan"].create(fsp_vals)
            new_move.write(
                {
                    "shipment_plan_id": forward_shipment_plan.id,
                }
            )
        return new_move


class SaleRentalRouteInLine(models.TransientModel):
    _inherit = "sale.rental.route.in.line"

    # (override)
    @api.multi
    def _split_rental_move(self):
        new_move = super()._split_rental_move()
        # (Extension) Create Forward Shipment Plan
        if self.move_id.shipment_plan_id and self.rental_out_move_id.shipment_plan_id:
            order_lines = self.env["sale.order.line"].browse()
            order_lines |= self.rental_id.start_order_line_id
            order_lines |= self.rental_out_id.start_order_line_id
            fsp_vals = self.env["shipment.plan"]._prepare_forward_shipment_plan_values(
                self.move_id.shipment_plan_id, self.rental_out_move_id.shipment_plan_id
            )
            forward_shipment_plan = self.env["shipment.plan"].create(fsp_vals)
            new_move.write(
                {
                    "shipment_plan_id": forward_shipment_plan.id,
                }
            )
