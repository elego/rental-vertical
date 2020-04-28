# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    toll_line_ids = fields.One2many(
        'toll.charge.line',
        'toll_contract_id',
        string='Toll Charge Lines',
    )

    @api.model
    def _finalize_invoice_creation(self, invoices):
        res = super(ContractContract, self)._finalize_invoice_creation(invoices)
        toll_amount = 0.0
        if invoices:
            for line in invoices.invoice_line_ids:
                open_toll_lines = line.product_id.get_open_road_charges()
                if open_toll_lines:
                    toll_amount += line.product_id.get_open_road_charges_amount()
            if toll_amount:
                toll_line_inv = self.prepare_toll_line_inv(toll_amount, invoices)
                self.add_toll_lines_on_invoice(open_toll_lines, invoices)
        return res

    @api.multi
    def prepare_toll_line_inv(self, toll_amount, invoices):
        toll_product_id = self.env.ref('rental_toll_collect.product_maut')
        account_analytic_id = self.env.ref(
            'rental_toll_collect.account_analytic_account_maut')
        journal_id = invoices.journal_id
        account_id = journal_id.default_credit_account_id
        toll_line_inv = self.env['account.invoice.line'].create({
                'product_id': toll_product_id.id or False,
                'name': 'Road charges (Maut)',
                'start_date': invoices.date_invoice,
                'uom_id': toll_product_id.uom_id.id,
                'end_date': self.recurring_next_date,
                'must_have_dates': True,
                'quantity': 1.0,
                'price_unit': toll_amount,
                'invoice_id': invoices.id,
                'account_analytic_id': account_analytic_id.id,
                'account_id': account_id.id or False,
                'invoice_line_tax_ids': [(4, account_id.tax_ids[0].id)]
            })
        return toll_line_inv

    @api.multi
    def add_toll_lines_on_invoice(self, open_toll_lines, invoices):
        toll_lines =[]
        # set is_charges=True for all invoices toll lines
        for line in open_toll_lines:
            line.is_charges = True
            toll_lines.append(line.id)
        invoices.toll_line_ids = [(6, 0, toll_lines)]
