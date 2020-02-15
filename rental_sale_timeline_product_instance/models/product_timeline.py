# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    product_instance_state = fields.Selection(
        related="product_id.instance_state",
    )
    product_instance_next_service_date = fields.Date(
        related="product_id.instance_next_service_date",
    )
    product_instance_current_location_id = fields.Many2one(
        related="product_id.instance_current_location_id",
    )
    product_instance_serial_number_id = fields.Many2one(
        related="product_id.instance_serial_number_id",
    )
