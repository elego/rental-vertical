# Copyright 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016 Sodexis (http://sodexis.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
        if 'onsite_location_id' in values:
            res['location_dest_id'] = values['onsite_location_id']
        return res

class StockMove(models.Model):
    _inherit = "stock.move"

    rental_out_id = fields.Many2one(
        "sale.rental", "Rental (out)", copy=False, ondelete="restrict"
    )
    rental_in_id = fields.Many2one(
        "sale.rental", "Rental (in)", copy=False, ondelete="restrict"
    )

    @api.multi
    def _action_cancel(self):
        """
        increase the quantity of origin move.
        """
        for move in self:
            if move.rental_out_id:
                if move.rental_out_id.out_move_id.state == "done":
                    raise UserError(
                        _(
                            'The outgoing move of the \
                        referenced rental is in state "done".'
                        )
                    )
                else:
                    move.rental_out_id.out_move_id.product_uom_qty += (
                        move.product_uom_qty
                    )
                    move.rental_out_id.out_move_id.ordered_qty = (
                        move.rental_out_id.out_move_id.product_uom_qty
                    )
            if move.rental_in_id:
                if move.rental_in_id.in_move_id.state == "done":
                    raise UserError(
                        _(
                            'The return move of the \
                        referenced rental is in state "done".'
                        )
                    )
                else:
                    move.rental_in_id.in_move_id.product_uom_qty += (
                        move.product_uom_qty
                    )
                    move.rental_in_id.in_move_id.ordered_qty = (
                        move.rental_in_id.in_move_id.product_uom_qty
                    )
        return super(StockMove, self)._action_cancel()

    def _push_apply(self):
        if self.env.context.get("do_not_push_apply", False):
            return True
        else:
            return super(StockMove, self)._push_apply()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    rental_order = fields.Many2one(
        "sale.order",
        "Rental Order",
        copy=False,
        ondelete="restrict",
        help="Order which caused (created) the picking as rental (in)",
    )
