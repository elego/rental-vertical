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

    update_toll_lines = fields.Boolean(
        string="Update Toll Charge Lines",
        compute="_compute_update_toll_lines"
    )

    @api.multi
    def _compute_toll_charged_count(self):
        for rec in self:
            rec.toll_line_charged_count = len(rec.order_line.mapped('toll_line_ids').filtered('invoiced'))

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.order_line.mapped('toll_line_ids'))

    @api.multi
    def _compute_update_toll_lines(self):
        for rec in self:
            rec.update_toll_lines = any(rec.order_line.mapped('update_toll_lines'))

    @api.multi
    def action_view_product_toll_charges(self):
        self.ensure_one()
        record_ids = self.order_line.mapped('toll_line_ids').ids
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
    def action_update_toll_charges(self):
        for order in self:
            for line in order.order_line:
                line.update_toll_charge_lines()
        return True

    @api.multi
    def _finalize_invoices(self, invoices, references):
        res = super()._finalize_invoices(invoices, references)
        for invoice in invoices.values():
            if invoice.partner_id.administrative_charge:
                product = invoice.partner_id.administrative_charge_product
                self.env['account.invoice.line']._create_administrative_product_line(invoice, product)
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    toll_line_ids = fields.One2many(
        comodel_name='toll.charge.line',
        inverse_name='sale_line_id',
        string="Toll Charge Lines",
    )

    update_toll_lines = fields.Boolean(
        string='Update Toll Charge Lines',
        default=False,
    )

    @api.onchange(
        'product_id',
        'start_date',
        'end_date',
    )
    def onchange_toll_lines_params(self):
        self.update_toll_lines = True

    @api.model_create_multi
    def create(self, values):
        so_lines = super().create(values)
        for line in so_lines:
            line.update_toll_charge_lines()
        return so_lines

    @api.multi
    def update_toll_charge_lines(self):
        self.ensure_one()
        if not self.display_type:
            toll_charge_lines = self.env['toll.charge.line'].search([
                ('product_id', 'in', [self.product_id.id, self.display_product_id.id]),
                ('toll_date', '>=', self.start_date),
                ('toll_date', '<=', self.end_date),
                '|',
                ('sale_line_id', '=', False),
                ('sale_line_id', '=', self.id),
            ])
            self.write({
                'toll_line_ids': [(6, 0, toll_charge_lines.ids)],
                'update_toll_lines': False,
            })

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.update_toll_charge_lines()
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({
            'toll_line_ids': [(6, 0, self.toll_line_ids.filtered(lambda l: not l.invoiced).ids)],
        })
        return res
