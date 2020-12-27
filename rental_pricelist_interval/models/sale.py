# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rental_interval_price = fields.Boolean(
        string="Use Interval Price",
    )
    show_rental_interval_price = fields.Boolean(
        string="Show Option Interval Price",
    )
    rental_interval_name = fields.Char(
        string="Rental Interval",
    )

    @api.multi
    def _update_show_rental_interval_price(self):
        uom_day = self.env.ref("uom.product_uom_day")
        self.ensure_one()
        if self.rental and self.product_uom.id == uom_day.id:
            self.show_rental_interval_price = True
        else:
            self.show_rental_interval_price = False
            self.rental_interval_price = False

    @api.multi
    def _get_interval_price(self):
        self.ensure_one()
        res = False
        uom_day = self.env.ref("uom.product_uom_day")
        if self.rental_interval_price and self.product_uom.id == uom_day.id:
            product = self.product_id.rented_product_id
            if product and product.rental_of_interval:
                uom_qty = self.number_of_time_unit
                if uom_qty > product.rental_interval_max:
                    raise UserError(
                        _("Max rental interval (%s days) is exceeded.")
                        % product.rental_interval_max
                    )
                for item in product.rental_price_interval_item_ids:
                    if uom_qty >= item.min_quantity:
                        res = item
                if not res:
                    raise UserError(_("No found suitable interval price."))
        return res

    @api.multi
    def _update_interval_price(self):
        self.ensure_one()
        if self.product_id.rented_product_id and self.rental_interval_price:
            price_item = self._get_interval_price()
            if not price_item:
                return
            self.product_uom_qty = 1
            self.price_unit = price_item.price * self.rental_qty
            self.rental_interval_name = price_item.name

    @api.multi
    @api.onchange("product_id")
    def product_id_change(self):
        res = super().product_id_change()
        if self.product_id.rented_product_id.rental_of_interval:
            self.rental_interval_price = True
        return res

    @api.onchange("product_id", "rental_qty")
    def rental_product_id_change(self):
        res = super().rental_product_id_change()
        self._update_show_rental_interval_price()
        self._update_interval_price()
        return res

    @api.onchange("rental_qty", "number_of_time_unit", "product_id")
    def rental_qty_number_of_days_change(self):
        res = super().rental_qty_number_of_days_change()
        self._update_show_rental_interval_price()
        self._update_interval_price()
        return res

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        self._update_show_rental_interval_price()
        self._update_interval_price()
        return res

    @api.onchange("start_date", "end_date", "product_uom")
    def onchange_start_end_date(self):
        res = super().onchange_start_end_date()
        if self.start_date and self.end_date:
            self._update_interval_price()
        return res

    @api.onchange("rental_interval_price")
    def onchange_rental_interval_price(self):
        if self.rental_interval_price:
            self._update_interval_price()
        else:
            self.product_uom_change()
