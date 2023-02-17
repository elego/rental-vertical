# Copyright 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016 Sodexis (http://sodexis.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    rental_out_id = fields.Many2one(
        comodel_name="sale.rental",
        string="Rental (out)",
        copy=False,
        ondelete="restrict",
    )

    rental_in_id = fields.Many2one(
        comodel_name="sale.rental",
        string="Rental (in)",
        copy=False,
        ondelete="restrict",
    )

    def _action_cancel(self):
        """
        increase the quantity of origin move.
        """
        for move in self:
            if move.rental_out_id:
                if move.rental_out_id.out_move_id.state == "done":
                    raise UserError(
                        _(
                            "The outgoing move of the referenced rental is in state 'Done'."
                        )
                    )
                else:
                    move.rental_out_id.out_move_id.product_uom_qty += (
                        move.product_uom_qty
                    )
            if move.rental_in_id:
                if move.rental_in_id.in_move_id.state == "done":
                    raise UserError(
                        _(
                            "The return move of the referenced rental is in state 'Done'."
                        )
                    )
                else:
                    move.rental_in_id.in_move_id.product_uom_qty += move.product_uom_qty
        return super(StockMove, self)._action_cancel()

    def _push_apply(self):
        if self.env.context.get("do_not_push_apply", False):
            return True
        else:
            return super(StockMove, self)._push_apply()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    rental_order = fields.Many2one(
        comodel_name="sale.order",
        string="Rental Order",
        copy=False,
        ondelete="restrict",
        help="This is the order that created the picking as rental (in).",
    )


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        """Inherit to write the end date of the rental on the return move"""
        res = super(StockRule, self)._push_prepare_move_copy_values(
            move_to_copy, new_date
        )
        location_id = res.get("location_id", False)
        if (
            location_id
            and move_to_copy.sale_line_id
            and move_to_copy.sale_line_id.order_id.partner_shipping_id.rental_onsite_location_id
            and location_id
            == move_to_copy.sale_line_id.order_id.partner_shipping_id.rental_onsite_location_id.id
            and move_to_copy.sale_line_id.rental_type == "new_rental"
        ):
            rental_end_date = move_to_copy.sale_line_id.end_date
            res["date"] = fields.Datetime.to_datetime(rental_end_date)
        return res
