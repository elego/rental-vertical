# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)
# TODO : block if we sell a rented product already sold => state


class SaleRental(models.Model):
    _inherit = "sale.rental"

    out_move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="rental_out_id",
        copy=False,
        help="Moves that are splitted from out_move_id",
    )

    in_move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="rental_in_id",
        copy=False,
        help="Moves that are splitted from in_move_id",
    )

    out_move_id_bk = fields.Many2one(
        comodel_name="stock.move",
        string="Outgoing Stock Moves BK",
    )

    in_move_id_bk = fields.Many2one(
        comodel_name="stock.move",
        string="Return Stock Moves BK",
    )

    rental_onsite_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Onsite location",
        related="start_order_line_id.order_id.partner_shipping_id.rental_onsite_location_id",
    )

    # (override)
    @api.depends(
        "start_order_line_id.order_id.state",
        "start_order_line_id.move_ids.state",
        "start_order_line_id.move_ids.move_dest_ids.state",
        "sell_order_line_ids.move_ids.state",
        "in_move_ids.state",
        "out_move_ids.state",
    )
    def _compute_move_and_state(self):
        for rental in self:
            # procurement = False
            in_move = False
            out_move = False
            # sell_procurement = False
            sell_move = False
            state = False
            if rental.start_order_line_id:
                if rental.start_order_line_id.move_ids:
                    # (change) set in_move and out_move just one time
                    # in_move_id_bk and out_move_id_bk are already
                    # be set in fuction _prepare_rental
                    if not rental.in_move_id_bk or not rental.out_move_id_bk:
                        for move in rental.start_order_line_id.move_ids:
                            if move.move_dest_ids:
                                out_move = move
                                in_move = move.move_dest_ids[0]
                    else:
                        in_move = rental.in_move_id_bk
                        out_move = rental.out_move_id_bk
                if (
                    rental.sell_order_line_ids
                    and rental.sell_order_line_ids[0].move_ids
                ):
                    sell_move = rental.sell_order_line_ids[0].move_ids[0]
                state = "ordered"
                # set state by checking state of in_move, out_move,
                # in_move_ids and out_move_ids
                if out_move and in_move:
                    in_moves_done_qty = 0
                    out_moves_done_qty = 0
                    if rental.in_move_ids:
                        for m in rental.in_move_ids:
                            if m.state == "done":
                                in_moves_done_qty += m.product_qty
                    if rental.out_move_ids:
                        for m in rental.out_move_ids:
                            if m.state == "done":
                                out_moves_done_qty += m.product_qty
                    if (
                        out_move.state == "done"
                        and out_moves_done_qty
                        == rental.rental_qty - out_move.product_qty
                    ):
                        state = "out"
                    if (
                        out_move.state == "done"
                        and in_move.state == "done"
                        and out_moves_done_qty
                        == rental.rental_qty - out_move.product_qty
                        and in_moves_done_qty == rental.rental_qty - in_move.product_qty
                    ):
                        state = "in"
                    if sell_move:
                        state = "sell_progress"
                        if sell_move.state == "done":
                            state = "sold"
                        elif sell_move.state == "cancel":
                            state = "out"
                if rental.start_order_line_id.order_id.state == "cancel":
                    state = "cancel"
            if in_move:
                rental.in_move_id = in_move
                rental.in_move_id_bk = in_move
            if out_move:
                rental.out_move_id = out_move
                rental.out_move_id_bk = out_move
            rental.state = state
            rental.sell_move_id = sell_move
