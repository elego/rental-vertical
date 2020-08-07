# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.start_date')
    def _compute_default_start_date(self):
        for order in self:
            dates = []
            so_lines = order.order_line
            if so_lines:
                for line in so_lines:
                    if line.start_date:
                        dates.append(line.start_date)
            if dates:
                order.update({
                    'default_start_date': min(dates),
                    })

    @api.depends('order_line.end_date')
    def _compute_default_end_date(self):
        for order in self:
            dates = []
            so_lines = order.order_line
            if so_lines:
                for line in so_lines:
                    if line.end_date:
                        dates.append(line.end_date)
            if dates:
                order.update({
                    'default_end_date': min(dates),
                    })


    default_start_date = fields.Date(string='Default Start Date',
            compute='_compute_default_start_date', readonly=False)
    default_end_date = fields.Date(string='Default End Date',
            compute='_compute_default_end_date', readonly=False)

    @api.multi
    def unlink(self):
        for rec in self:
            rentals = self.env['sale.rental'].search([
                ('start_order_line_id', 'in', rec.order_line.ids),
            ])
            rentals.unlink()
        res = super().unlink()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    rental_qty_uom = fields.Many2one(
        string="Product Unit of Measure",
        related='product_id.rented_product_id.uom_id',
    )

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.product_id.income_analytic_account_id:
            res['account_analytic_id'] = self.product_id.income_analytic_account_id.id
        return res
