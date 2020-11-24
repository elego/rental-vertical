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
