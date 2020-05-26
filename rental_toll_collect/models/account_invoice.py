# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    toll_line_ids = fields.One2many(
        comodel_name='toll.charge.line',
        inverse_name='invoice_id',
        string="Toll Charge Lines",
    )

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
            rec.toll_line_charged_count = len(rec.toll_line_ids)

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.get_product_toll_charges())

    @api.multi
    def get_product_toll_charges(self):
        self.ensure_one()
        toll_charge_lines = self.env['toll.charge.line']

        for line in self.invoice_line_ids:
            if line.product_id:
                # Only products or related rental products with license plate can have toll charge lines.
                if line.product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.id),
                        ('toll_date', '>=', line.start_date),
                        ('toll_date', '<=', line.end_date),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', '=', self.id),
                    ])
                elif line.product_id.rented_product_id and line.product_id.rented_product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.rented_product_id.id),
                        ('toll_date', '>=', line.start_date),
                        ('toll_date', '<=', line.end_date),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', '=', self.id),
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
                            ('invoice_id', '=', self.id),
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

    @api.multi
    def create_toll_charge_invoice_lines(self, values):
        self.ensure_one()
        invoice_line_context = {
            'type': self.type,
            'journal_id': self.journal_id.id,
            'default_invoice_id': self.id,
        }
        invoice_line_obj = self.env['account.invoice.line'].with_context(invoice_line_context)
        toll_charge_product = self.env.ref('rental_toll_collect.product_toll')
        for key, value in values.items():
            line = invoice_line_obj.create({
                'product_id': toll_charge_product.id,
                'name': toll_charge_product.display_name + " for " + key.license_plate,
                'quantity': sum(value['distance']),
                'uom_id': toll_charge_product.uom_id.id,
                'price_unit': sum(value['amount']) / sum(value['distance']),  # TODO: check total amount, rounding!!!
                'start_date': min(value['date']).date(),
                'end_date': max(value['date']).date(),
                'account_analytic_id': key.income_analytic_account_id.id if key.income_analytic_account_id else False,
            })
            # line._onchange_product_id()
            # line._onchange_uom_id()
            # line._onchange_account_id()

    @staticmethod
    def get_toll_charge_invoice_line_values(toll_lines):
        values = {product: {'amount': [], 'date': [], 'distance': [], }
                  for product in toll_lines.mapped('product_id')}
        for tcl in toll_lines:
            values[tcl.product_id]['amount'].append(tcl.amount)
            values[tcl.product_id]['date'].append(tcl.toll_date)
            values[tcl.product_id]['distance'].append(tcl.distance)
        return values
