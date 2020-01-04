# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _
from odoo.tools import float_compare

import math


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    number_of_time_unit = fields.Float('Number of TU')
    display_product_id = fields.Many2one('product.product', string='Product')
    rental_ok = fields.Boolean('Can be Rented', related="display_product_id.rental_ok")
    #must_have_dates = fields.Boolean(string="Must Have Dates", related=False)

    @api.model
    def _get_time_uom(self):
        uom_month = self.env.ref('sale_rental_pricelist.product_uom_month')
        uom_day = self.env.ref('uom.product_uom_day')
        uom_hour = self.env.ref('uom.product_uom_hour')
        return {
            'month': uom_month,
            'day': uom_day,
            'hour': uom_hour,
        }

    @api.multi
    def _set_product_id(self):
        self.ensure_one()
        if self.rental and self.display_product_id:
            time_uoms = self._get_time_uom()
            if self.display_product_id.rental_of_day:
                self.product_uom = time_uoms['day']
                self.product_id = self.display_product_id.product_rental_day_id
            elif self.display_product_id.rental_of_day:
                self.product_uom = time_uoms['month']
                self.product_id = self.display_product_id.product_rental_month_id
            elif self.display_product_id.rental_of_hour:
                self.product_uom = time_uoms['hour']
                self.product_id = self.display_product_id.product_rental_hour_id
            else:
                raise exceptions.UserError(_('No Found Service Product for Rental.'))
           

    @api.multi
    @api.onchange('display_product_id')
    def onchange_display_product_id(self):
        if self.display_product_id:
            self.product_id = self.display_product_id
            self.rental = False
            self.can_sell_rental = False

    @api.multi
    @api.onchange('rental')
    def onchange_rental(self):
        if self.rental:
            self.can_sell_rental = False
            self.sell_rental_id = False
        else:
            self.rental_type = False
            self.rental_qty = 0
            self.extension_rental_id = False
        self._set_product_id()

    @api.multi
    @api.onchange('can_sell_rental')
    def onchange_can_sell_rental(self):
        if self.can_sell_rental:
            self.rental = False
            self.rental_type = False
            self.rental_qty = 0
            self.extension_rental_id = False
        else:
            self.sell_rental_id = False
        self.product_id = self.display_product_id

    #Override function in sale_rental
    @api.onchange('product_id', 'rental_qty')
    def rental_product_id_change(self):
        res = {}
        if self.product_id:
            if self.product_id.rented_product_id:
                #self.rental = True
                #self.can_sell_rental = False
                self.sell_rental_id = False
                if not self.rental_type:
                    self.rental_type = 'new_rental'
                elif (
                        self.rental_type == 'new_rental' and
                        self.rental_qty and self.order_id.warehouse_id):
                    product_uom = self.product_id.rented_product_id.uom_id
                    warehouse = self.order_id.warehouse_id
                    rental_in_location = warehouse.rental_in_location_id
                    rented_product_ctx = \
                        self.with_context(
                            location=rental_in_location.id
                        ).product_id.rented_product_id
                    in_location_available_qty =\
                        rented_product_ctx.qty_available -\
                        rented_product_ctx.outgoing_qty
                    compare_qty = float_compare(
                        in_location_available_qty, self.rental_qty,
                        precision_rounding=product_uom.rounding)
                    if compare_qty == -1:
                        res['warning'] = {
                            'title': _("Not enough stock !"),
                            'message': _(
                                "You want to rent %.2f %s but you only "
                                "have %.2f %s currently available on the "
                                "stock location '%s' ! Make sure that you "
                                "get some units back in the mean time or "
                                "re-supply the stock location '%s'.") % (
                                self.rental_qty,
                                product_uom.name,
                                in_location_available_qty,
                                product_uom.name,
                                rental_in_location.name,
                                rental_in_location.name)
                        }
            elif self.product_id.rental_service_ids:
                #self.can_sell_rental = True
                #self.rental = False
                self.rental_type = False
                self.rental_qty = 0
                self.extension_rental_id = False
            else:
                self.rental_type = False
                #self.rental = False
                self.rental_qty = 0
                self.extension_rental_id = False
                #self.can_sell_rental = False
                self.sell_rental_id = False
        else:
            self.rental_type = False
            #self.rental = False
            self.rental_qty = 0
            self.extension_rental_id = False
            #self.can_sell_rental = False
            self.sell_rental_id = False
        return res

    #Override function in sale_rental
    @api.constrains(
        'rental_type', 'extension_rental_id', 'start_date', 'end_date',
        'rental_qty', 'product_uom_qty', 'product_id')
    def _check_sale_line_rental(self):
        for line in self:
            if line.rental_type == 'rental_extension':
                if not line.extension_rental_id:
                    raise ValidationError(_(
                        "Missing 'Rental to Extend' on the sale order line "
                        "with rental service %s") % line.product_id.name)

                if line.rental_qty != line.extension_rental_id.rental_qty:
                    raise ValidationError(_(
                        "On the sale order line with rental service %s, "
                        "you are trying to extend a rental with a rental "
                        "quantity (%s) that is different from the quantity "
                        "of the original rental (%s). This is not supported.")
                        % (
                        line.product_id.name,
                        line.rental_qty,
                        line.extension_rental_id.rental_qty))
            if line.rental_type in ('new_rental', 'rental_extension'):
                if not line.product_id.rented_product_id:
                    raise ValidationError(_(
                        "On the 'new rental' sale order line with product "
                        "'%s', we should have a rental service product !") % (
                        line.product_id.name))
                #if line.product_uom_qty !=\
                #        line.rental_qty * line.number_of_days:
                #    raise ValidationError(_(
                #        "On the sale order line with product '%s' "
                #        "the Product Quantity (%s) should be the "
                #        "number of days (%s) "
                #        "multiplied by the Rental Quantity (%s).") % (
                #        line.product_id.name, line.product_uom_qty,
                #        line.number_of_days, line.rental_qty))
                # the module sale_start_end_dates checks that, when we have
                # must_have_dates, we have start + end dates
            elif line.sell_rental_id:
                if line.product_uom_qty != line.sell_rental_id.rental_qty:
                    raise ValidationError(_(
                        "On the sale order line with product %s "
                        "you are trying to sell a rented product with a "
                        "quantity (%s) that is different from the rented "
                        "quantity (%s). This is not supported.") % (
                        line.product_id.name,
                        line.product_uom_qty,
                        line.sell_rental_id.rental_qty))

    #Override function in sale_rental
    #replace number_of_days with number_of_time_unit
    @api.onchange('rental_qty', 'number_of_time_unit', 'product_id')
    def rental_qty_number_of_days_change(self):
        if self.product_id.rented_product_id:
            qty = self.rental_qty * self.number_of_time_unit
            self.product_uom_qty = qty

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.rental and 'domain' in res and 'product_uom' in res['domain']:
            del(res['domain']['product_uom'])
            if self.display_product_id.rental_ok:
                time_uoms = self._get_time_uom()
                uom_ids = []
                if self.display_product_id.rental_of_month:
                    uom_ids.append(time_uoms['month'].id)
                if self.display_product_id.rental_of_day:
                    uom_ids.append(time_uoms['day'].id)
                if self.display_product_id.rental_of_hour:
                    uom_ids.append(time_uoms['hour'].id)
                res['domain']['product_uom'] = [('id', 'in', uom_ids)]
        return res

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.display_product_id and self.product_uom and self.rental:
            if self.product_uom.id != self.product_id.uom_id:
                time_uoms = self._get_time_uom()
                for key in time_uoms:
                    if self.product_uom.id == time_uoms[key].id:
                        self.product_id = self.display_product_id._get_rental_service(key)
                        break
        return super(SaleOrderLine, self).product_uom_change()

    @api.onchange('start_date', 'end_date', 'product_uom')
    def onchange_start_end_date(self):
        if self.start_date and self.end_date:
            number = False
            time_uoms = self._get_time_uom()
            if self.product_uom.id == time_uoms['day'].id: 
                number = (self.end_date - self.start_date).days + 1
            elif self.product_uom.id == time_uoms['hour'].id:
                number = ((self.end_date - self.start_date).days + 1) * 8
            elif self.product_uom.id == time_uoms['month'].id:
                number = ((self.end_date - self.start_date).days + 1) / 30
                number = math.ceil(number)
            self.number_of_time_unit = number
