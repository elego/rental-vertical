# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class SaleRentalRouteOutLine(models.TransientModel):
    _inherit = "sale.rental.route.out.line"

    #(override)
    @api.multi
    def _split_rental_move(self):
        self.ensure_one()
        if not self.rental_in_id:
            return False
        rounding = self.product_id.uom_id.rounding
        if (
            float_compare(
                self.rental_avail_qty, self.qty, precision_rounding=rounding
            )
            < 0
        ):
            raise UserError(
                _(
                    "You can not reorder the Rental, available \
                quantity is less then the required quantity."
                )
            )
        # Moves for rented product use always the default uom of the product.
        # So we don't need to compute the quantity in uom of move.
        self.move_id.product_uom_qty -= self.qty
        new_picking = self.rental_in_move_id.picking_id.copy(
            {
                "move_lines": [],
                "location_id": self.rental_in_move_id.location_id.id,
                "location_dest_id": self.move_id.location_dest_id.id,
                "rental_order": self.rental_in_id.start_order_line_id.order_id.id,
            }
        )
        reset_qty = False
        if (
            float_compare(
                self.rental_in_move_id.product_qty,
                self.qty,
                precision_rounding=rounding,
            )
            == 0
        ):
            self.rental_in_move_id.product_uom_qty += 1
            reset_qty = True
        new_move_id = self.rental_in_move_id.with_context(
            do_not_push_apply=True
        )._split(self.qty)
        if reset_qty:
            self.rental_in_move_id.product_uom_qty -= 1
        new_move = self.env["stock.move"].browse(new_move_id)
        # (Extension) Create Forward Shipment Plan
        order_lines = self.env['sale.order.line'].browse()
        order_lines |= self.rental_id.start_order_line_id
        order_lines |= self.rental_in_id.start_order_line_id
        fsp_vals = self.env['shipment.plan']._prepare_forward_shipment_plan_values(
            self.rental_in_move_id.shipment_plan_id,
            self.move_id.shipment_plan_id
        )
        forward_shipment_plan = self.env['shipment.plan'].create(fsp_vals)
        new_move.write(
            {
                "location_id": self.rental_in_move_id.location_id.id,
                "location_dest_id": self.move_id.location_dest_id.id,
                "rental_in_id": self.rental_in_id.id,
                "rental_out_id": self.rental_id.id,
                "group_id": self.move_id.group_id.id,
                #'procurement_id': self.move_id.procurement_id.id,
                "picking_id": new_picking.id,
                # (Extension) Set Forward Shipment Plan
                "shipment_plan_id": forward_shipment_plan.id,
            }
        )


class SaleRentalRouteInLine(models.TransientModel):
    _inherit = "sale.rental.route.in.line"

    #(override)
    @api.multi
    def _split_rental_move(self):
        self.ensure_one()
        if not self.rental_out_id:
            return False
        rounding = self.product_id.uom_id.rounding
        if (
            float_compare(
                self.rental_avail_qty, self.qty, precision_rounding=rounding
            )
            < 0
        ):
            raise UserError(
                _(
                    "You can not reorder the Rental, \
                available quantity is less then the required quantity."
                )
            )
        # Moves for rented product use always the default uom of the product.
        # So we don't need to compute the quantity in uom of move.
        self.move_id.product_uom_qty -= self.qty
        new_picking = self.move_id.picking_id.copy(
            {
                "move_lines": [],
                "location_id": self.move_id.location_id.id,
                "location_dest_id": self.rental_out_move_id.location_dest_id.id,
                "rental_order": self.rental_id.start_order_line_id.order_id.id,
            }
        )
        reset_qty = False
        if (
            float_compare(
                self.rental_out_move_id.product_qty,
                self.qty,
                precision_rounding=rounding,
            )
            == 0
        ):
            self.rental_out_move_id.product_uom_qty += 1
            reset_qty = True
        new_move_id = self.rental_out_move_id.with_context(
            do_not_push_apply=True
        )._split(self.qty)
        if reset_qty:
            self.rental_out_move_id.product_uom_qty -= 1
        new_move = self.env["stock.move"].browse(new_move_id)
        # (Extension) Create Forward Shipment Plan
        order_lines = self.env['sale.order.line'].browse()
        order_lines |= self.rental_id.start_order_line_id
        order_lines |= self.rental_out_id.start_order_line_id
        fsp_vals = self.env['shipment.plan']._prepare_forward_shipment_plan_values(
            self.move_id.shipment_plan_id,
            self.rental_out_move_id.shipment_plan_id
        )
        forward_shipment_plan = self.env['shipment.plan'].create(fsp_vals)
        new_move.write(
            {
                "location_id": self.move_id.location_id.id,
                "location_dest_id": self.rental_out_move_id.location_dest_id.id,
                "rental_out_id": self.rental_out_id.id,
                "rental_in_id": self.rental_id.id,
                "group_id": self.rental_out_move_id.group_id.id,
                #'procurement_id': self.rental_out_move_id.procurement_id.id,
                "picking_id": new_picking.id,
                # (Extension) Set Forward Shipment Plan
                "shipment_plan_id": forward_shipment_plan.id,
            }
        )
