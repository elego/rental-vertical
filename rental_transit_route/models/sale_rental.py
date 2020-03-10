# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)

class SaleRental(models.Model):
    _inherit = "sale.rental"

    @api.depends(
        'sell_order_line_ids.move_ids.state',
        'start_order_line_id.order_id.state',
        'start_order_line_id.move_ids.state',
        'start_order_line_id.move_ids.move_dest_ids.state')
    def _compute_move_and_state(self):
        for rental in self:
            in_move = False
            out_move = False
            sell_move = False
            state = False
            if rental.start_order_line_id:
                for move in rental.start_order_line_id.move_ids:
                    #if move.state != 'cancel':
                    #    out_move = move
                    #if move.move_dest_ids:
                    #    out_move = move
                    #    in_move = move.move_dest_ids[0]
                    if move.picking_type_id.code == 'outgoing':
                        out_move = move
                    elif move.picking_type_id.code == 'incoming':
                        in_move = move
                if rental.sell_order_line_ids and\
                        rental.sell_order_line_ids[0].move_ids:
                    sell_move = rental.sell_order_line_ids[0].move_ids[-1]
                state = 'ordered'
                if out_move and out_move.state == 'done':
                    state = 'out'
                    if in_move:
                        if in_move.state == 'done':
                            state = 'in'
                        elif in_move.state == 'cancel' and sell_move:
                            state = 'sell_progress'
                            if sell_move.state == 'done':
                                state = 'sold'
                    elif sell_move:
                        state = 'sell_progress'
                        if sell_move.state == 'done':
                            state = 'sold'
                        elif sell_move.state == 'cancel':
                            state = 'out'
                if rental.start_order_line_id.state == 'cancel':
                    state = 'cancel'
            rental.in_move_id = in_move
            rental.out_move_id = out_move
            rental.state = state
            rental.sell_move_id = sell_move
