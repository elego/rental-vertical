# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import _, models, fields, exceptions
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit="stock.move"

    rental_out_line_id = fields.Many2one(
        comodel_name="rental.stock.product.line",
    )
    rental_in_line_id = fields.Many2one(
        comodel_name="rental.stock.product.line",
    )
    rental_out_move_id = fields.Many2one(
        comodel_name="stock.move",
        related="rental_out_line_id.out_move_id",
    )
    rental_in_move_id = fields.Many2one(
        comodel_name="stock.move",
        related="rental_in_line_id.in_move_id",
    )

    def _action_cancel(self):
        for move in self:
            rounding = move.product_id.uom_id.rounding
            if move.rental_out_move_id and move.rental_out_move_id.state != "cancel":
                if move.rental_out_move_id.state == "done":
                    raise exceptions.UserError(
                        _("You can not cancel the move that are linked with the rental out move in state 'Done'")
                    )
                reset_qty = move.product_uom_qty
                if (
                    float_compare(
                        move.product_uom_qty,
                        move.rental_out_line_id.reduced_qty_out,
                        precision_rounding=rounding,
                    )
                    > 0
                ):
                    reset_qty = move.rental_out_line_id.reduced_qty_out
                    reset_increased_qty = move.product_uom_qty - move.rental_out_line_id.reduced_qty_out
                    move.rental_out_line_id.in_move_id.product_uom_qty -= reset_increased_qty
                move.rental_out_move_id.product_uom_qty += reset_qty
                move.rental_out_line_id.reduced_qty_out -= reset_qty
                move.rental_out_line_id.routed_qty_out -= move.product_uom_qty
            if move.rental_in_move_id and move.rental_in_move_id.state != "cancel":
                if move.rental_in_move_id.state == "done":
                    raise exceptions.UserError(
                        _("You can not cancel the move that are linked with the rental in move in state 'Done'")
                    )
                move.rental_in_move_id.product_uom_qty += move.product_uom_qty
                move.rental_in_line_id.reduced_qty_in -= move.product_uom_qty
                move.rental_in_line_id.routed_qty_in -= move.product_uom_qty
        return super()._action_cancel()
