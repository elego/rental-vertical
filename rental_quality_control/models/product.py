# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    inspections_count = fields.Integer(compute='_compute_inspections_count',
                                       string="Inspections Count",
                                       type='integer')

    @api.multi
    def _compute_inspections_count(self):
        QcInspection = self.env['qc.inspection']
        for product in self:
            product.inspections_count = QcInspection.search_count(
                [('product_id', '=', product.id)])