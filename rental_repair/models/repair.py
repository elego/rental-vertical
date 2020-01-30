# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    project_task_id = fields.Many2one('project.task', 'Task', ondelete="set null")

    income_analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Income Analytic Account',
        company_dependent=True)
    expense_analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Expense Analytic Account',
        company_dependent=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(RepairOrder, self).onchange_product_id()
        if self.product_id:
            self.income_analytic_account_id = self.product_id.income_analytic_account_id.id
            self.expense_analytic_account_id = self.product_id.expense_analytic_account_id.id

    @api.multi
    def action_invoice_create(self, group=False):
        res = super(RepairOrder, self).action_invoice_create(group=group)
        for repair in self:
            if repair.income_analytic_account_id:
                analytic_id = repair.income_analytic_account_id.id
                for operation in repair.operations:
                    if operation.invoiced and operation.invoice_line_id:
                        operation.invoice_line_id.account_analytic_id = analytic_id
                for fee in repair.fees_lines:
                    if fee.invoiced and fee.invoice_line_id:
                        fee.invoice_line_id.account_analytic_id = analytic_id
        return res
