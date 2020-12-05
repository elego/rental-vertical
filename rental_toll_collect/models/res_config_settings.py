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
