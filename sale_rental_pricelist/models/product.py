# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.tools import float_compare

import math

class ProductTemplate(models.Model):

    _inherit = "product.template"

    rental_ok = fields.Boolean('Can be Rented')

class ProductProduct(models.Model):

    _inherit = "product.product"

    def _default_pricelist(self):
        # TODO change default pricelist if country group exist
        return self.env.ref('product.list0').id

    rental_of_month = fields.Boolean('Rented in Month', copy=False)
    rental_of_day = fields.Boolean('Rented in day', copy=False)
    rental_of_hour = fields.Boolean('Rented in hour', copy=False)
    product_rental_month_id = fields.Many2one('product.product', 'Rental Service (Month)', ondelete="set null", copy=False)
    product_rental_day_id = fields.Many2one('product.product', 'Rental Service (Day)', ondelete="set null", copy=False)
    product_rental_hour_id = fields.Many2one('product.product', 'Rental Service (Hour)', ondelete="set null", copy=False)
    rental_price_month = fields.Float(
        string='Price / Month',
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_month_id.list_price")
    rental_price_day = fields.Float(
        string='Price / Day',
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_day_id.list_price")
    rental_price_hour = fields.Float(
        string='Price / Hour',
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_hour_id.list_price")
    day_scale_pricelist_item_ids = fields.One2many('product.pricelist.item', 'day_item_id', string='Day Scale Pricelist Items', copy=False)
    month_scale_pricelist_item_ids = fields.One2many('product.pricelist.item', 'month_item_id', string='Month Scale Pricelist Items', copy=False)
    hour_scale_pricelist_item_ids = fields.One2many('product.pricelist.item', 'hour_item_id', string='Hour Scale Pricelist Items', copy=False)
    def_pricelist_id = fields.Many2one('product.pricelist', 'Default Pricelist', default=lambda self: self._default_pricelist())

    @api.multi
    def _get_rental_service(self, rental_type):
        self.ensure_one()
        if rental_type == 'month' and self.product_rental_month_id:
            return self.product_rental_month_id
        elif rental_type == 'day' and self.product_rental_day_id:
            return self.product_rental_day_id
        elif rental_type == 'hour' and self.product_rental_hour_id:
            return self.product_rental_hour_id
        else:
            raise exceptions.ValidationError(_('No found Rental Service.'))

    @api.model
    def _create_rental_service(self, rental_type, product, price=0):
        time_uoms = self.env['sale.order.line']._get_time_uom()
        uom = False
        if rental_type == 'month':
            uom = time_uoms['month']
        elif rental_type == 'day':
            uom = time_uoms['day']
        elif rental_type == 'hour':
            uom = time_uoms['hour']
        else:
            raise exceptions.ValidationError(_('No found expected Rental Type.'))
        values = {
            'hw_product_id': product.id,
            'name': _('Rental of %s (%s)') %(product.name, uom.name),
            'categ_id': product.categ_id.id,
            'copy_image': True,
        }
        res = self.env['create.rental.product'].with_context(
            active_model="product.product", active_id=product.id).create(values).create_rental_product()
        rental_service = self.browse(res['res_id'])
        rental_service.write({
            'uom_id': uom.id,
            'uom_po_id': uom.id,
            'rental_ok': True,
            'income_analytic_account_id': product.income_analytic_account_id.id,
            'expense_analytic_account_id': product.expense_analytic_account_id.id,
            'list_price': price})
        return rental_service

    @api.multi
    def _update_rental_service_analytic_account(self, vals):
        self.ensure_one()
        income_analytic_account_id = vals.get('income_analytic_account_id', False)
        expense_analytic_account_id = vals.get('expense_analytic_account_id', False)
        self.rental_service_ids.write({
            'income_analytic_account_id': income_analytic_account_id,
            'expense_analytic_account_id': expense_analytic_account_id})

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        for p in self:
            # Create service product automatically
            if vals.get('rental_of_month', False):
                if not p.product_rental_month_id:
                    service_product = self._create_rental_service('month', p, p.rental_price_month)
                    p.product_rental_month_id = service_product
            if vals.get('rental_of_day', False):
                if not p.product_rental_day_id:
                    service_product = self._create_rental_service('day', p, p.rental_price_day)
                    p.product_rental_day_id = service_product
            if vals.get('rental_of_hour', False):
                if not p.product_rental_hour_id:
                    service_product = self._create_rental_service('hour', p, p.rental_price_hour)
                    p.product_rental_hour_id = service_product
            # update analytic account for service product
            p._update_rental_service_analytic_account(vals)

    @api.model
    def create(self, vals):
        ext_vals = {}
        if vals.get('rental_of_month', False):
            ext_vals['rental_of_month'] = True
            ext_vals['rental_price_month'] = vals.get('rental_price_month')
            del(vals['rental_of_month'])
            if 'rental_price_month' in vals:
                del(vals['rental_price_month'])
        if vals.get('rental_of_day', False):
            ext_vals['rental_of_day'] = True
            ext_vals['rental_price_day'] = vals.get('rental_price_day')
            del(vals['rental_of_day'])
            if 'rental_price_day' in vals:
                del(vals['rental_price_day'])
        if vals.get('rental_of_hour', False):
            ext_vals['rental_of_hour'] = True
            ext_vals['rental_price_hour'] = vals.get('rental_price_hour')
            del(vals['rental_of_hour'])
            if 'rental_price_hour' in vals:
                del(vals['rental_price_hour'])
        res = super().create(vals)
        res.write(ext_vals)
        return res
