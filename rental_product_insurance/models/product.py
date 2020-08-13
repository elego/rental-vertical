# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_insurance = fields.Boolean(
        string='Insurance',
        default=False,
        help='This product is a insurance.',
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('none', 'None'),
            ('product', 'Cost of Product'),
            ('rental', 'Cost of Rental'),
        ],
        default="none",
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )
