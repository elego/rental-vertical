# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from datetime import timedelta
import time


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_offday = fields.Boolean("Show Off Day", compute="_compute_show_offday")
    offday_number = fields.Float("Number of off days", compute="_compute_offday_number")
    add_offday_ids = fields.One2many('rental.offday', 'add_order_line_id', string='Additional Off Days')
    fixed_offday_ids = fields.One2many('rental.offday', 'fixed_order_line_id', string='Fixed Off Days')
    fixed_offday_type = fields.Selection(string="Off Day Type",
        selection=[
            ('none', 'none'),
            ('weekend', 'Weekend'),
            #('weekend_holiday', 'Weekend and Holiday'),
        ], default="none")

    @api.depends('product_uom')
    def _compute_show_offday(self):
        uom_day = self.env.ref('uom.product_uom_day')
        for line in self:
            line.show_offday = False
            if line.product_uom.id == uom_day.id:
                line.show_offday = True

    @api.depends('fixed_offday_ids', 'add_offday_ids')
    def _compute_offday_number(self):
        self.offday_number = len(self.fixed_offday_ids) + len(self.add_offday_ids)

    @api.model
    def is_weekend(self, date):
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        if time.strptime(date.strftime("%Y-%m-%d"),'%Y-%m-%d').tm_wday in (5,6):
            return True
        return False

    @api.model
    def get_rental_offdays(self, date_from, date_to):
        if isinstance(date_from, str):
            date_from = fields.Date.from_string(date)
        if isinstance(date_to, str):
            date_to = fields.Date.from_string(date)
        weekends = []
        res = {
            'weekends': weekends,
        }
        if not date_from or not date_to:
            return res
        if date_from > date_to:
            if self._context.get('no_warning', False):
                return res
            else:
                raise exceptions.Warning(_('The start date must be anterior to the end date.'))
        date_first = date_from
        date_last = date_to
        date_next = date_first
        while date_next <= date_last:
            if self.is_weekend(date_next):
                weekends.append(date_next)
            date_next = date_next + timedelta(days=1)
        res = {
            'weekends': weekends,
        }
        return res

    @api.onchange('fixed_offday_type', 'start_date', 'end_date')
    def onchange_fixed_offday_type(self):
        offday_obj = self.env['rental.offday']
        #values of one2many field fixed_offday_ids
        values = [(5, 0, 0)]
        if self.fixed_offday_type == 'none':
            self.fixed_offday_ids = values
        if self.fixed_offday_type == 'weekend':
            dic_offdays = self.get_rental_offdays(self.start_date, self.end_date)
            weekends = dic_offdays and dic_offdays['weekends'] or False
            if weekends:
                for d in weekends:
                    values.append((0, 0, {'date': d, 'name': 'Weekend'}))
            self.fixed_offday_ids = values
        if self.start_date and self.end_date:
            for day in self.add_offday_ids:
                if day.date < self.start_date or day.date > self.end_date:
                    raise exceptions.UserError(_('You can not add the off day "%s" between %s and %s') % (day.date, self.start_date, self.end_date))
                

    #Override function in sale_rental
    #replace number_of_days with number_of_time_unit
    @api.onchange('offday_number', 'rental_qty', 'number_of_time_unit', 'product_id')
    def rental_qty_number_of_days_change(self):
        if self.product_id.rented_product_id:
            qty = self.rental_qty * self.number_of_time_unit
            if self.show_offday:             
                qty = self.rental_qty * (self.number_of_time_unit - self.offday_number)
            self.product_uom_qty = qty

    @api.onchange('add_offday_ids', 'start_date', 'end_date')
    def onchange_add_offday_ids(self):
        if self.add_offday_ids:
            dates = []
            for day in self.add_offday_ids:
                if not day.date:
                    continue
                if day.date < self.start_date or day.date > self.end_date:
                    raise exceptions.UserError(_('You can not add the off day "%s" between %s and %s') % (day.date, self.start_date, self.end_date))
                if day.date in [d.date for d in self.fixed_offday_ids]:
                    raise exceptions.UserError(_('off day %s was already created as fixed off day.') % day.date)
                if day.date not in dates:
                    dates.append(day.date)
                else:
                    raise exceptions.UserError(_('You have already created the off day %s') % day.date)
