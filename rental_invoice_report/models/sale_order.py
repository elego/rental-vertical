# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_name = fields.Char(
        string="Name of Branch",
        help="Please enter here the name of the company branch. "
             "It will be printed on report.",
    )
