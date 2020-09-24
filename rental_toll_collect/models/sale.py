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
            rec.toll_line_charged_count = sum(
                [len(invoice.toll_line_ids.filtered('invoiced')) for invoice in self.invoice_ids]
            )

    @api.multi
    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.order_line.mapped('toll_line_ids'))

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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    toll_line_ids = fields.One2many(
        comodel_name='toll.charge.line',
        inverse_name='sale_line_id',
        string="Toll Charge Lines",
    )

    @api.multi
    def write(self, values):
        if not self.display_type:
            products = [
                values.get('product_id', self.product_id.id),
                values.get('display_product_id', self.display_product_id.id),
            ]
            start_date = fields.Date.to_date(values.get('start_date')) or self.start_date
            end_date = fields.Date.to_date(values.get('end_date')) or self.end_date
            toll_charge_lines = self.env['toll.charge.line'].search([
                ('product_id', 'in', products),
                ('toll_date', '>=', start_date),
                ('toll_date', '<=', end_date),
                '|',
                ('invoice_id', '=', False),
                ('invoice_id', 'in', self.order_id.invoice_ids.ids),
            ])
            values.update({
                'toll_line_ids': [(6, 0, toll_charge_lines.ids)],
            })
        return super(SaleOrderLine, self).write(values)

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({
            'toll_line_ids': [(6, 0, self.toll_line_ids.ids)],
        })
        return res
