# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.depends('toll_line_ids.toll_charge', 'toll_line_ids.is_charges')
    def _compute_road_charges(self):
        for rec in self:
            rec.toll_charge_count = len(rec.toll_line_ids)

    toll_line_ids = fields.One2many(
        'toll.charge.line',
        'toll_invoice_id',
        string='Toll Charge Lines',
    )
    toll_charge_count = fields.Integer(
        compute='_compute_road_charges',
        string="Toll Charges",
        type='integer')

    @api.multi
    def action_view_toll_charges(self):
        self.ensure_one()
        record_ids = [line.id for line in self.toll_line_ids]
        action = self.env.ref('rental_toll_collect.toll_charge_line_action').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action
