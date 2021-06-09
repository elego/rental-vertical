# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(selection_add=[("rental", "Rental")])
    origin_return_sale_line_ids = fields.One2many(
        "sale.order.line",
        "trans_return_shipment_plan_id",
        "Origin Return Sale Order Lines",
    )

    @api.multi
    def _get_transport_pr_name(self):
        self.ensure_one()
        if self.env.context.get("rental_return", False):
            return _("Inbound transport for %s") % (self.origin)
        return _("Outbound transport for %s") % (self.origin)

class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        values,
        group_id,
    ):
        res = super(StockRule, self)._get_stock_move_values(
            product_id=product_id,
            product_qty=product_qty,
            product_uom=product_uom,
            location_id=location_id,
            name=name,
            origin=origin,
            values=values,
            group_id=group_id,
        )
        if values.get("shipment_plan_id", False):
            res["shipment_plan_id"] = values.get("shipment_plan_id")
        return res

    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        """Inherit to write the date of the rental on move"""
        # get value of return move
        res = super(StockRule, self)._push_prepare_move_copy_values(
            move_to_copy, new_date
        )
        if move_to_copy.sale_line_id and move_to_copy.sale_line_id.rental:
            return_shipment_plan_id = (
                move_to_copy.sale_line_id.trans_return_shipment_plan_id
            )
            if return_shipment_plan_id:
                res["shipment_plan_id"] = return_shipment_plan_id.id
        return res
