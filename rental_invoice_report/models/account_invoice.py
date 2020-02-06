# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    branch_name = fields.Char(string="Name of Branch")
    date_start = fields.Date(string="Date Start")
    date_end = fields.Date(dtring="Date End")
