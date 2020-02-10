# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    offday_number = fields.Float('Off days', related="sale_order_line_id.offday_number")
