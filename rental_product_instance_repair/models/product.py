# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def action_view_project_task(self):
        res = super(ProductProduct, self).action_view_project_task()
        if self.product_instance and self.instance_serial_number_id:
            lot_id = self.instance_serial_number_id.id
            res['context']['default_lot_id'] = lot_id
        return res
