# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions, _


class ResCompany(models.Model):
    _inherit = "res.company"

    automatic_toll_charge_invoicing = fields.Boolean(
        string="Automatic Toll Charges Invoicing",
        help="If activated, imported toll charge lines are "
             "automatically invoiced when invoicing a sale "
             "or rental order or contract.",
    )
    administrative_charge = fields.Boolean(
        string="Administrative Charge",
        help="If activated,you can set your own default "
        "administrative charge product for the partners.",
        default=True,
    )
    administrative_charge_product = fields.Many2one(
        comodel_name="product.product",
        string="Administrative Charge Product",
        default=lambda self: self.env.ref(
            'rental_toll_collect.product_administrative_charge',
            raise_if_not_found=False
        ),
        domain=[('type', '=', 'service')],
        help="Product that can be used as default "
        "administrative charge product for the partners.",
    )

    @api.model
    def create(self, values):
        company = super(ResCompany, self).create(values)
        company._set_administrative_charge_product()
        return company

    def _set_administrative_charge_product(self):
        for company in self:
            if not company.administrative_charge_product:
                product = self.env.ref('rental_toll_collect.product_administrative_charge')
                company.write({
                    'administrative_charge_product': product.id,
                })
