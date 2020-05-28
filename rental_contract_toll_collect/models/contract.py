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
        string="# Toll Charge Lines",
        type='integer',
    )

    @api.multi
    def _compute_toll_charged_count(self):
        for rec in self:
            rec.toll_line_charged_count = sum([
                len(invoice.toll_line_ids) for invoice in self._get_related_invoices()
            ])

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.get_product_toll_charges())

    @api.multi
    def get_product_toll_charges(self):
        """
        This method returns the id of all toll charge lines related to the given products in contract lines,
        for the entire time of the contract line (date_start till date_end).
        :return: list of toll charge line ids for contract's total period
        """
        self.ensure_one()
        toll_charge_lines = self.env['toll.charge.line']

        for line in self.contract_line_ids:
            if line.product_id:
                # Only products or related rental products with license plate can have toll charge lines.
                if line.product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.id),
                        ('toll_date', '>=', line.date_start),
                        ('toll_date', '<=', line.date_end),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', 'in', self._get_related_invoices().ids),
                    ])
                elif line.product_id.rented_product_id and line.product_id.rented_product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.rented_product_id.id),
                        ('toll_date', '>=', line.date_start),
                        ('toll_date', '<=', line.date_end),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', 'in', self._get_related_invoices().ids),
                    ])
                # After manually invoicing toll charge lines the "real" product can only be found by analytic account.
                elif line.product_id == self.env.ref('rental_toll_collect.product_toll'):
                    product = self.env['product.product'].search([
                        ('income_analytic_account_id', '=', line.account_analytic_id.id),
                    ])
                    if product:
                        toll_charge_lines |= self.env['toll.charge.line'].search([
                            ('product_id', 'in', product.ids),
                            ('toll_date', '>=', line.date_start),
                            ('toll_date', '<=', line.date_end),
                            '|',
                            ('invoice_id', '=', False),
                            ('invoice_id', 'in', self._get_related_invoices().ids),
                        ])
        return list(set(toll_charge_lines.mapped('id')))

    @api.multi
    def get_product_toll_charges_current_period(self):
        """
        This method returns the id of all toll charge lines related to the given products in contract lines,
        for the current invoice period.
        It is not possible to use next_period_date_start and next_period_date_end, since both dates are updated
        before finalizing the invoice (in method _prepare_recurring_invoices_values from contract lines).
        So, the period end is last_date_invoiced, and the period start can be calculated from last_date_invoiced,
        recurring_interval and recurring_rule_type.
        :return: list of toll charge line ids for contract's current invoice period
        """
        self.ensure_one()
        toll_charge_lines = self.env['toll.charge.line']

        for line in self.contract_line_ids:
            if line.product_id:
                # See method comment
                date_start = line._get_previous_period_date_start()
                date_end = line.last_date_invoiced
                # Only products or related rental products with license plate can have toll charge lines.
                if line.product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.id),
                        ('toll_date', '>=', date_start),
                        ('toll_date', '<=', date_end),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', 'in', self._get_related_invoices().ids),
                    ])
                elif line.product_id.rented_product_id and line.product_id.rented_product_id.license_plate:
                    toll_charge_lines |= self.env['toll.charge.line'].search([
                        ('product_id', '=', line.product_id.rented_product_id.id),
                        ('toll_date', '>=', date_start),
                        ('toll_date', '<=', date_end),
                        '|',
                        ('invoice_id', '=', False),
                        ('invoice_id', 'in', self._get_related_invoices().ids),
                    ])
                # After manually invoicing toll charge lines the "real" product can only be found by analytic account.
                elif line.product_id == self.env.ref('rental_toll_collect.product_toll'):
                    product = self.env['product.product'].search([
                        ('income_analytic_account_id', '=', line.account_analytic_id.id),
                    ])
                    if product:
                        toll_charge_lines |= self.env['toll.charge.line'].search([
                            ('product_id', 'in', product.ids),
                            ('toll_date', '>=', date_start),
                            ('toll_date', '<=', date_end),
                            '|',
                            ('invoice_id', '=', False),
                            ('invoice_id', 'in', self._get_related_invoices().ids),
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

    def _finalize_invoice_creation(self, invoices):
        """
        When creating the invoice from contract, the invoice lines for toll charges will be added,
        before calling the super-method.
        :param invoices: current invoices to be created from contract
        """
        for invoice in invoices:
            tcls = self.env['toll.charge.line'].browse(self.get_product_toll_charges_current_period())
            tcls = tcls.filtered(lambda l: l.chargeable and not l.invoiced)
            values = invoice.get_toll_charge_invoice_line_values(tcls)
            invoice.create_toll_charge_invoice_lines(values)
            for tcl in tcls:
                tcl.write({'invoice_id': invoice.id, })
        super(ContractContract, self)._finalize_invoice_creation(invoices)


class ContractLine(models.Model):
    _inherit = 'contract.line'

    def _get_previous_period_date_start(self):
        self.ensure_one()
        if self.last_date_invoiced:
            relative = self.get_relative_delta(self.recurring_rule_type, self.recurring_interval)
            prev_period_date_start = self.last_date_invoiced - relative + relativedelta(days=1)
        else:
            # This should not happen because the last_date_invoiced is set after preparing the first invoice
            # for this contract line and before creating its invoice lines. So, the invoice would not have been
            # created yet and then the creation of invoice lines would be weird.
            raise exceptions.ValidationError(
                _("Something bad happened during invoice creation. "
                  "The 'Last Date Invoiced' should have been set but it was not.")
            )
        return prev_period_date_start
