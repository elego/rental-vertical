# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(
        selection_add=[("sale", "Sale")],
    )

    origin_sale_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="trans_shipment_plan_id",
        string="Origin Sale Order Lines",
        copy=False,
    )

    sale_id = fields.Many2one(
        comodel_name="sale.order",
        string="Origin Sale Order",
        compute="_compute_sale_id",
    )

    @api.depends("origin_sale_line_ids")
    def _compute_sale_id(self):
        for record in self:
            if record.origin_sale_line_ids:
                record.sale_id = record.origin_sale_line_ids[0].order_id
