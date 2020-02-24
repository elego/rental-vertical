# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    ceo_name = fields.Char(string="Name of CEO")
