# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools


class ResPartner(models.Model):
    _inherit = 'res.partner'

    administrative_charge = fields.Boolean(
        string="Administrative Charge",
        help="If activated, an invoice line with the administrative charge product "
             "is added to the invoice when invoicing toll charge lines.",
        default=True,
    )

    administrative_charge_product = fields.Many2one(
        comodel_name="product.product",
        string='Charge Product',
        default=lambda self: self.env.ref(
            'rental_toll_collect.product_administrative_charge',
            raise_if_not_found=False
        ),
        domain=[('type', '=', 'service')],
    )
