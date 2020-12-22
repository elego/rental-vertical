# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    transport_sales_margin = fields.Float(
        "Transport Sales Margin (%)",
        default=0,
    )
