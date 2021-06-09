# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_transport = fields.Boolean(
        "Transport Service",
        copy=True,
        help="If set, it allows the user to create a transport request or call for tender in order to find a carrier delivering the chosen products.",
    )
    trans_purchase_request = fields.Boolean(
        "Transport required",
        copy=True,
    )

class ProductProduct(models.Model):
    _inherit = "product.product"

    transport_service_type = fields.Selection(
        [
            ("po", "Purchase Order"),
            ("pr", "Purchase Requisition"),
        ],
        default="po",
    )
