# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_transport = fields.Boolean(
        string="Transport Service",
        copy=True,
    )

    trans_purchase_request = fields.Boolean(
        string="Transport required",
        copy=True,
        help="If set, it allows the user to create a transport "
             "request or call for tender in order to find a carrier "
             "delivering the chosen products.",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    transport_service_type = fields.Selection(
        selection=[
            ("po", "Purchase Order"),
            ("pr", "Purchase Requisition"),
        ],
        default="po",
        help="The transport request type defines if a purchase "
             "order or a call for tender is created when requesting "
             "a transport within an order.",
    )
