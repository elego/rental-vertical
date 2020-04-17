# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(
        selection_add=[('rental', 'Rental')]
    )
    origin_return_sale_line_ids = fields.One2many(
        'sale.order.line',
        'trans_return_shipment_plan_id',
        'Origin Return Sale Order Lines',
    )

