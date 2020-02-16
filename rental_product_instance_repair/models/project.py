# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_instance = fields.Boolean(
        'Product Instance',
        related="product_id.product_instance")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.lot_id = self.product_id.instance_serial_number_id
