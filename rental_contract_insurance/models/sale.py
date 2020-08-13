# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    day_insurance_product_ids = fields.Many2many(
        'product.product',
        'day_insurance_product_rel',
        'product_id',
        'day_product_id',
        string='Insurance Products (Day)',
        domain=lambda self: [
            ('uom_id', '=', self.env.ref('uom.product_uom_day').id),
            ('is_insurance', '=', True),
        ],
    )
    month_insurance_product_ids = fields.Many2many(
        'product.product',
        'month_insurance_product_rel',
        'product_id',
        'month_product_id',
        string='Insurance Products (Month)',
        domain=lambda self: [
            ('uom_id', '=', self.env.ref('rental_base.product_uom_month').id),
            ('is_insurance', '=', True),
        ],
    )

    @api.constrains('is_insurance', 'uom_id')
    def _check_insurance_uom(self):
        res = self.search([
            ('is_insurance', '=', True),
            ('uom_id.category_id', '!=', self.env.ref('uom.uom_categ_wtime')),
        ])
        if res:
            raise exceptions.ValidationError(
                _('Uom of Insurance product should be in Category Time.'))

    def _get_insurance_product(self, uom):
        self.ensure_one()
        uom_day = self.env.ref('uom.product_uom_day')
        uom_month = self.env.ref('rental_base.product_uom_month')
        res = self.browse()
        if uom == uom_day:
            res = self.day_insurance_product_ids
        elif uom == uom_month:
            res = self.month_insurance_product_ids
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insurance_entire_time = fields.Boolean(
        'Insurance for entire Time',
        default=True,
    )

    #override
    @api.onchange('product_id', 'product_uom')
    def onchange_insurance_product_id(self):
        self.insurance_type = 'none'
        if self.product_id:
            if self.product_id.rented_product_id:
                rented_product = self.product_id.rented_product_id
                self.insurance_type = rented_product.insurance_type
                self.insurance_percent = rented_product.insurance_percent
                self.insurance_product_ids = rented_product._get_insurance_product(self.product_uom)
            else:
                self.insurance_type = self.product_id.insurance_type
                self.insurance_percent = self.product_id.insurance_percent
                self.insurance_product_ids = self.product_id._get_insurance_product(self.product_uom)

    #override
    @api.onchange(
        'insurance_percent',
        'insurance_type',
        'product_uom_qty',
        'rental_qty',
        'price_unit',
        'insurance_entire_time',
        'number_of_time_unit',
    )
    def onchange_insurance_amount(self):
        insurance_amount = 0
        self.insurance_price_unit = 0
        percent = self.insurance_percent
        if self.insurance_type == 'product':
            price = self.product_id.rented_product_id.standard_price
            insurance_amount = price * percent / 100
        elif self.insurance_type == 'rental':
            insurance_amount = self.price_subtotal * percent / 100
        if self.rental and self.product_uom_qty:
            if self.insurance_entire_time and self.number_of_time_unit:
                self.insurance_price_unit = insurance_amount / self.number_of_time_unit
            else:
                self.insurance_price_unit = \
                    self.rental_qty * insurance_amount / self.product_uom_qty

    #override
    @api.onchange(
        'product_uom_qty',
        'product_uom',
        'price_unit',
        'insurance_percent',
        'insurance_type',
        'insurance_entire_time',
        'insurance_product_ids',
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

    def _prepare_rental_insurance_line(self, product):
        res = super()._prepare_rental_insurance_line(product)
        qty = self.product_uom_qty / self.rental_qty
        if self.insurance_entire_time:
            qty = self.number_of_time_unit
        res['product_uom_qty'] = qty
        return res

    @api.multi
    def update_rental_insurance_line(self):
        res = super().update_rental_insurance_line()
        if res:
            qty = self.product_uom_qty / self.rental_qty
            if self.insurance_entire_time:
                qty = self.number_of_time_unit
            res.write({
            'product_uom_qty': qty,
            })
        return res

    @api.multi
    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        res = super(SaleOrderLine, self)._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res['analytic_account_id'] = rental_product.income_analytic_account_id.id
        return res
