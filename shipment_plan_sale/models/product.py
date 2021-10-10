# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    transport_sales_margin = fields.Float(
        string="Transport Sales Margin (%)",
        default=0,
        help="This percent value defines how much more the "
             "customer has to pay for the transportation "
             "costs you are charged by the carrier.",
    )
