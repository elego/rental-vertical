# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contract_type = fields.Many2one(
        comodel_name='contract.order.type', string='Contract Order Type',
        company_dependent=True)
