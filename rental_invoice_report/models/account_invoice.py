# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    branch_name = fields.Char(
        string="Name of Branch",
        help="Please enter here the name of the company branch. "
             "It will be printed on report.",
    )
    date_start = fields.Date(
        string="Date Start",
        help="Please set here the start date of the service or delivery period. "
             "It will be printed on report, together with the given end date.",
    )
    date_end = fields.Date(
        string="Date End",
        help="Please set here the end date of the service or delivery period. "
             "It will be printed on report, together with the given start date.",
    )
