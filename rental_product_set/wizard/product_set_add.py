# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError

import math

class ProductSetAdd(models.TransientModel):
    _inherit = 'product.set.add'

    rental_ok = fields.Boolean('Can be Rented', default=False)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    uom_id = fields.Many2one('uom.uom', sting="Unit Of Measure")

    @api.model
    def _get_time_uom(self):
        time_uom = []
        uom_month = self.env.ref('rental_pricelist.product_uom_month')
        uom_day = self.env.ref('uom.product_uom_day')
        uom_hour = self.env.ref('uom.product_uom_hour')
        time_uom.extend([uom_month.id, uom_hour.id, uom_day.id])
        return time_uom

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(
                    _('The end date cannot be earlier than the start date.'))

    @api.multi
    def add_set(self):
        if self.rental_ok:
            uom_list = self._get_time_uom()
            sale_order_line = False
            so_id = self._context['active_id']
            if not so_id:
                return
            so = self.env['sale.order'].browse(so_id)
            max_sequence = 0
            if so.order_line:
                max_sequence = max([line.sequence for line in so.order_line])
            sale_order_line_env = self.env['sale.order.line']
            sale_order_line = self.env['sale.order.line']
            for set_line in self.product_set_id.set_line_ids:
                if set_line.product_id.rental_service_ids and set_line.product_id.rental_ok:
                    for rent_product in set_line.product_id.rental_service_ids:
                        if self.uom_id.id in uom_list:
                            if self.uom_id.id == rent_product.uom_id.id:
                                sale_order_line |= sale_order_line_env.create(
                                self.prepare_rental_so_line(
                                    so_id, set_line, rent_product, rent_product.uom_id,
                                    max_sequence=max_sequence))
        else:
            sale_order_line = super(ProductSetAdd, self).add_set()
        return sale_order_line

    @api.multi
    def prepare_rental_so_line(self, sale_order_id, set_line, product, uom_id, max_sequence):
        line_data = self.env['sale.order.line'].new({
                'order_id': sale_order_id,
                'product_id': product.id,
                'display_product_id': product.id,
                'product_uom_qty': set_line.quantity * self.quantity,
                'product_uom': uom_id.id,
                'sequence': max_sequence + set_line.sequence,
                'discount': set_line.discount,
                'start_date': self.start_date,
                'end_date': self.end_date,
            })
        line_data.product_id_change()
        line_data.onchange_start_end_date()
        line_values = line_data._convert_to_write(line_data._cache)
        return line_values

    @api.onchange('product_set_id')
    def _onchange_product_set_id(self):
        if self.product_set_id and self.rental_ok:
            time_uom = []
            uom_list = self._get_time_uom()
            for set_line in self.product_set_id.set_line_ids:
                if set_line.product_id.rental_service_ids and set_line.product_id.rental_ok:
                    for rent_product in set_line.product_id.rental_service_ids:
                        if rent_product.uom_id.id in uom_list:
                            time_uom.append(rent_product.uom_id.id)
                else:
                    raise ValidationError(
                        _("From Product set %s : %s must be marked 'Can be Rented' and "
                          "its service products must be available.")
                        % (self.product_set_id.name, set_line.product_id.name))
            if time_uom:
                time_uom = list(set(time_uom))
                self.uom_id = time_uom[0]
                return {'domain': {'uom_id': [('id', 'in', time_uom)]}}
