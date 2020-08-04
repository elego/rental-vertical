# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.start_date')
    def _compute_default_start_date(self):
        for order in self:
            so_lines = order.order_line
            if so_lines:
                for i in range(len(so_lines)):
                    default_start_date = so_lines[0].start_date
                    if i > 0 and so_lines[i].start_date:
                        if so_lines[i].start_date <= default_start_date:
                            default_start_date = so_lines[i].start_date
                order.update({
                    'default_start_date': default_start_date,
                    })

    @api.depends('order_line.end_date')
    def _compute_default_end_date(self):
        for order in self:
            so_lines = order.order_line
            if so_lines:
                for i in range(len(so_lines)):
                    default_end_date = so_lines[0].end_date
                    if i > 0 and so_lines[i].end_date:
                        if so_lines[i].end_date >= default_end_date:
                            default_end_date = so_lines[i].end_date
                order.update({
                    'default_end_date': default_end_date,
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

    @api.model
    def _get_time_uom(self):
        uom_month = self.env.ref('rental_base.product_uom_month')
        uom_day = self.env.ref('uom.product_uom_day')
        uom_hour = self.env.ref('uom.product_uom_hour')
        return {
            'month': uom_month,
            'day': uom_day,
            'hour': uom_hour,
        }

    @api.multi
    def _get_number_of_time_unit(self):
        self.ensure_one()
        number = False
        time_uoms = self._get_time_uom()
        if self.product_uom.id == time_uoms['day'].id:
            number = (self.end_date - self.start_date).days + 1
        elif self.product_uom.id == time_uoms['hour'].id:
            number = ((self.end_date - self.start_date).days + 1) * 8
        elif self.product_uom.id == time_uoms['month'].id:
            # ref link to calculate months (why 30.4167 ?)
            # https://www.checkyourmath.com/convert/time/days_months.php
            number = ((self.end_date - self.start_date).days + 1) / 30.4167
            number = float_round(number, precision_rounding=1)
        return number
