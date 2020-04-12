# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(
        selection_add=[('sale', 'Sale')]
    )
    origin_sale_line_ids = fields.One2many(
        'sale.order.line',
        'trans_shipment_plan_id',
        'Origin Sale Order Lines',
    )
    sale_id = fields.Many2one(
        'sale.order',
        'Origin Sale Order',
        compute="_compute_sale_id"
    )

    def _compute_sale_id(self):
        for record in self:
            if record.origin_sale_line_ids:
                record.sale_id = record.origin_sale_line_ids[0].order_id
