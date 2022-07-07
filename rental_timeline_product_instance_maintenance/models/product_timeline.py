# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    product_instance_next_service_date = fields.Date(
        related="product_id.instance_next_service_date",
        store=True,
    )
