# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        template = self.env.ref('rental_contract.rental_contract_template')
        res = super(ProductProduct, self).write(vals)
        for p in self:
            if vals.get('rental_of_month', False):
                if p.product_rental_month_id:
                    p.product_rental_month_id.is_contract = True
                    p.product_rental_month_id.property_contract_template_id = template.id
