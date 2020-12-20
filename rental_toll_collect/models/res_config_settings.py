# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    automatic_toll_charge_invoicing = fields.Boolean(
        string="Automatic Toll Charges Invoicing",
        help="If activated, imported toll charge lines are "
             "automatically invoiced when invoicing a sale "
             "or rental order or contract.",
        related="company_id.automatic_toll_charge_invoicing",
        readonly=False,
    )
    administrative_charge = fields.Boolean(
        string="Administrative Charge",
        related="company_id.administrative_charge",
        readonly=False,
        help="If activated,you can set your own default "
        "administrative charge product for the partners.",
    )
    administrative_charge_product = fields.Many2one(
        comodel_name="product.product",
        string="Administrative Charge Product",
        help="Product that can be used as default "
        "administrative charge product for the partners.",
        related="company_id.administrative_charge_product",
        domain="[('type', '=', 'service'),('company_id', '=', company_id)]",
        readonly=False,
    )

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        if self.administrative_charge_product and self.administrative_charge:
            company = self.env.user.company_id
            customers = self.env['res.partner'].search([('company_id', '=', company.id)])
            customers.write({
                'administrative_charge_product': self.administrative_charge_product.id,
            })
        return res
