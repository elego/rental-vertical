# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_instance = fields.Boolean(
        'Product Instance',
        related="product_id.product_instance")
