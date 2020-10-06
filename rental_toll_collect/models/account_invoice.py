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

    update_toll_lines = fields.Boolean(
        string="Update Toll Charge Lines",
        compute="_compute_update_toll_lines"
    )

    @api.multi
    def _compute_toll_charged_count(self):
        for rec in self:
            rec.toll_line_charged_count = len(rec.toll_line_ids.filtered('invoiced'))

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.toll_line_ids)

    @api.multi
    def _compute_update_toll_lines(self):
        for rec in self:
            rec.update_toll_lines = any(rec.invoice_line_ids.mapped('update_toll_lines'))

    @api.multi
    def action_view_product_toll_charges(self):
        self.ensure_one()
        tree_view_id = self.env.ref("rental_toll_collect.toll_charge_line_tree_view").id
        form_view_id = self.env.ref("rental_toll_collect.toll_charge_line_form_view").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Toll Charges'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'toll.charge.line',
            'domain': "[('id','in',[" + ','.join(map(str, self.toll_line_ids.ids)) + "])]",
            }

    @api.multi
    def action_update_toll_charges(self):
        for invoice in self:
            for line in invoice.invoice_line_ids:
                line.update_toll_charge_lines()
                if line.toll_line_ids:
                    if line.toll_product_line_ids:
                        vals = line._prepare_toll_product_line(line.toll_line_ids.filtered('chargeable'))
                        line.toll_product_line_ids.write(vals)
                    else:
                        line._create_toll_product_line()
                line.update_toll_lines = False
        return True


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    toll_line_ids = fields.One2many(
        comodel_name='toll.charge.line',
        inverse_name='invoice_line_id',
        string="Toll Charge Lines",
    )

    toll_product_origin_line_id = fields.Many2one(
        comodel_name="account.invoice.line",
        string="Origin for toll product invoice line",
        copy=False,
    )

    toll_product_line_ids = fields.One2many(
        comodel_name="account.invoice.line",
        inverse_name="toll_product_origin_line_id",
        string="Toll product invoice lines"
    )

    update_toll_lines = fields.Boolean(
        string="Update Toll Charge Lines",
        default=False,
    )

    @api.onchange(
        'product_id'
        'start_date',
        'end_date',
    )
    def onchange_toll_lines_params(self):
        self.update_toll_lines = True

    def _prepare_toll_product_line(self, chargeable_toll_lines):
        self.ensure_one()
        toll_charge_product = self.env.ref('rental_toll_collect.product_toll')
        uom_km = self.env.ref('uom.product_uom_km')
        distance = sum(chargeable_toll_lines.mapped('distance'))
        total_amount = sum(chargeable_toll_lines.mapped('amount'))
        license_plate = self.product_id.license_plate or self.product_id.rented_product_id.license_plate \
            if self.product_id.rented_product_id else ''
        account_id = self.get_invoice_line_account(
            self.invoice_id.type,
            toll_charge_product,
            self.invoice_id.fiscal_position_id,
            self.company_id
        )
        vals = {
            'product_id': toll_charge_product.id,
            'quantity': 1.0,
            'uom_id': toll_charge_product.uom_id.id,
            'price_unit': round(total_amount, 2),
            'name': toll_charge_product.display_name + _(" for ") + license_plate + _(" Total Distance: ") + str(round(distance, 2)) + " " + uom_km.name,
            'toll_product_origin_line_id': self.id,
            'invoice_id': self.invoice_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'account_id': account_id.id,
            'account_analytic_id': self.account_analytic_id.id if self.account_analytic_id else False,
        }
        return vals

    def _create_toll_product_line(self):
        self.ensure_one()
        chargeable_toll_lines = self.toll_line_ids.filtered('chargeable')
        vals = self._prepare_toll_product_line(chargeable_toll_lines)
        toll_product_line = self.env['account.invoice.line'].create(vals)
        return toll_product_line

    @api.multi
    def update_toll_charge_lines(self):
        self.ensure_one()
        if not self.display_type:
            rented_product_id = self.env['product.product'].browse(self.product_id.id).rented_product_id
            products = [self.product_id.id]
            if rented_product_id:
                products.append(rented_product_id.id)
            toll_charge_lines = self.env['toll.charge.line'].search([
                ('product_id', 'in', products),
                ('toll_date', '>=', self.start_date),
                ('toll_date', '<=', self.end_date),
                '|',
                ('invoice_id', '=', False),
                ('invoice_id', '=', self.invoice_id.id),
            ])
            self.write({
                'toll_line_ids': [(6, 0, toll_charge_lines.ids)],
                'update_toll_lines': False,
            })

    @api.model
    def create(self, vals):
        i_lines = super().create(vals)
        toll_product_lines = self.env['account.invoice.line']
        for line in i_lines:
            if not vals.get('toll_line_ids', False):
                line.update_toll_charge_lines()
            if line.toll_line_ids:
                toll_product_lines |= line._create_toll_product_line()
                line.update_toll_lines = False
        i_lines |= toll_product_lines
        return i_lines

    @api.multi
    def write(self, values):
        toll_lines = values.get('toll_line_ids', False)
        if toll_lines and any([item[2] for item in toll_lines]):
            values.update({
                'update_toll_lines': True
            })
        super(AccountInvoiceLine, self).write(values)
