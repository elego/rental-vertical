# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
            rec.toll_line_charged_count = sum([len(invoice.toll_line_ids) for invoice in self.invoice_ids])

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.get_product_toll_charges())

    @api.multi
    def get_product_toll_charges(self):
        self.ensure_one()
        toll_charge_lines = self.env['toll.charge.line']

        for line in self.order_line:
            if line.product_id:
                # Only products or related rental products with license plate can have toll charge lines.
                if line.product_id.license_plate or line.display_product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', 'in', [line.product_id.id, line.display_product_id.id]),
                        ('toll_date', '>=', line.start_date),
                        ('toll_date', '<=', line.end_date),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', 'in', self.invoice_ids.ids),
                    ])
                # After manually invoicing toll charge lines the "real" product can only be found by analytic account.
                elif line.product_id == self.env.ref('rental_toll_collect.product_toll'):
                    product = self.env['product.product'].search([
                        ('income_analytic_account_id', '=', line.account_analytic_id.id),
                    ])
                    if product:
                        toll_charge_lines |= self.env['toll.charge.line'].search([
                            ('product_id', 'in', product.ids),
                            ('toll_date', '>=', line.start_date),
                            ('toll_date', '<=', line.end_date),
                            '|',
                            ('invoice_id', '=', False),
                            ('invoice_id', '=', self.invoice_ids.ids),
                        ])
        return list(set(toll_charge_lines.mapped('id')))

    @api.multi
    def action_view_product_toll_charges(self):
        self.ensure_one()
        record_ids = self.get_product_toll_charges()
        tree_view_id = self.env.ref("rental_toll_collect.toll_charge_line_tree_view").id
        form_view_id = self.env.ref("rental_toll_collect.toll_charge_line_form_view").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Toll Charges'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'toll.charge.line',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    def _finalize_invoices(self, invoices, references):
        """
        When creating the invoice from sale order, the invoice lines for toll charges will be added,
        before calling the super-method.
        :param invoices: values of this dictionary contains the invoices
        :param references: dictionary contains the mapping of invoice and sale order
        """
        for invoice in invoices.values():
            tcls = self.env['toll.charge.line'].browse(references[invoice].get_product_toll_charges())
            tcls = tcls.filtered(lambda l: l.chargeable and not l.invoiced)
            values = invoice.get_toll_charge_invoice_line_values(tcls)
            invoice.create_toll_charge_invoice_lines(values)
            for tcl in tcls:
                tcl.write({'invoice_id': invoice.id, })
        super(SaleOrder, self)._finalize_invoices(invoices, references)
