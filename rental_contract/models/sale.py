# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('end_date')
    def end_date_change(self):
        res = super(SaleOrderLine, self).end_date_change()
        if self.end_date:
            self.date_end = self.end_date

    @api.onchange('start_date')
    def start_date_change(self):
        res = super(SaleOrderLine, self).start_date_change()
        if self.start_date:
            self.date_start = self.start_date
