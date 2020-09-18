# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from dateutil.relativedelta import relativedelta


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    toll_line_count = fields.Integer(
        compute='_compute_toll_line_count',
        string="# Toll Charge Lines",
        type='integer',
    )

    toll_line_charged_count = fields.Integer(
        compute='_compute_toll_charged_count',
        string="# Invoiced Toll Charge Lines",
        type='integer',
    )

    @api.multi
    def _compute_toll_charged_count(self):
        for rec in self:
            rec.toll_line_charged_count = sum([
                len(invoice.toll_line_ids.filtered('invoiced')) for invoice in self._get_related_invoices()
            ])

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.contract_line_ids.mapped('sale_order_line_id').mapped('toll_line_ids'))

    @api.multi
    def action_view_product_toll_charges(self):
        self.ensure_one()
        record_ids = self.contract_line_ids.mapped('sale_order_line_id').mapped('toll_line_ids')
        tree_view_id = self.env.ref("rental_toll_collect.toll_charge_line_tree_view").id
        form_view_id = self.env.ref("rental_toll_collect.toll_charge_line_form_view").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Toll Charges'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'toll.charge.line',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids.ids)) + "])]",
            }


class ContractLine(models.Model):
    _inherit = 'contract.line'

    @api.multi
    def _prepare_invoice_line(self, invoice_id=False, invoice_values=False):
        res = super(ContractLine, self)._prepare_invoice_line(invoice_id, invoice_values)
        start_date = fields.Date.to_date(res.get('start_date')) or self.next_period_date_start
        end_date = fields.Date.to_date(res.get('end_date')) or self.next_period_date_end
        if end_date and start_date:
            toll_charge_lines = self.sale_order_line_id.toll_line_ids.filtered(
                lambda l: end_date >= l.toll_date.date() >= start_date
            )
            res.update({
                'toll_line_ids': [(6, 0, toll_charge_lines.ids)],
            })
        return res
