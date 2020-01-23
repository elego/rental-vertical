# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ContractLine(models.Model):
    _inherit = 'contract.line'

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.contract_id.contract_type == 'sale':
                self.analytic_account_id = self.product_id.income_analytic_account_id
            elif self.contract_id.contract_type == 'purchase':
                self.analytic_account_id = self.product_id.expense_analytic_account_id

    @api.multi
    def _prepare_invoice_line(self, invoice_id=False):
        self.ensure_one()
        res = super(ContractLine, self)._prepare_invoice_line(invoice_id=invoice_id)
        product = self.env['product.product'].browse(res['product_id'])
        if product.must_have_dates:
            res.update({
                'start_date': self.next_period_date_start,
                'end_date': self.next_period_date_end,
            })
        return res
