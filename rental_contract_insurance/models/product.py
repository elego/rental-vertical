# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    day_insurance_product_ids = fields.One2many(
        'day.insurance.product.info',
        'product_id',
        string='Insurance Products (Day)',
    )
    month_insurance_product_ids = fields.One2many(
        'month.insurance.product.info',
        'product_id',
        string='Insurance Products (Month)',
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


class DayInsuranceProductInfo(models.Model):
    _name = 'day.insurance.product.info'
    _description = "Daily Insurances"

    product_id = fields.Many2one(
        'product.product',
        string='Rented Product'
    )
    insurance_product_id = fields.Many2one(
        'product.product',
        string='Insurance (Day)',
        domain=lambda self: [
            ('uom_id', '=', self.env.ref('uom.product_uom_day').id),
            ('is_insurance', '=', True),
        ],
    )
    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('product', 'Cost of Product'),
            ('rental', 'Cost of Rental'),
        ],
        default='product',
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )


class MonthInsuranceProductInfo(models.Model):
    _name = 'month.insurance.product.info'
    _description = "Monthly Insurances"

    product_id = fields.Many2one(
        'product.product',
        string='Rented Product'
    )
    insurance_product_id = fields.Many2one(
        'product.product',
        string='Insurance (Month)',
        domain=lambda self: [
            ('uom_id', '=', self.env.ref('rental_base.product_uom_month').id),
            ('is_insurance', '=', True),
        ],
    )
    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('product', 'Cost of Product'),
            ('rental', 'Cost of Rental'),
        ],
        default='product',
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )


class InsuranceProductSolInfo(models.Model):
    _name = 'insurance.product.sol.info'
    _description = "Insurance information on sale order line"

    sol_id = fields.Many2one(
        'sale.order.line',
        string='Order Line'
    )
    insurance_product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=lambda self: [
            ('is_insurance', '=', True),
        ],
    )
    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('product', 'Cost of Product'),
            ('rental', 'Cost of Rental'),
        ],
        default='product',
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )
    insurance_price_unit = fields.Float(
        'Insurance Amount',
        compute='_compute_insurance_price_unit'
    )

    #@api.depends(
    #    'insurance_percent',
    #    'insurance_type',
    #    'sol_id.product_uom_qty',
    #    'sol_id.rental_qty',
    #    'sol_id.price_unit',
    #    'sol_id.insurance_entire_time',
    #    'sol_id.number_of_time_unit',
    #)
    @api.multi
    def _compute_insurance_price_unit(self):
        for r in self:
            insurance_amount = 0
            r.insurance_price_unit = 0
            percent = r.insurance_percent
            if r.insurance_type == 'product':
                price = r.sol_id.product_id.rented_product_id.standard_price
                insurance_amount = price * percent / 100
            elif r.insurance_type == 'rental':
                insurance_amount = r.sol_id.price_subtotal * percent / 100
            if r.sol_id.rental and r.sol_id.product_uom_qty:
                if r.sol_id.insurance_entire_time and r.sol_id.number_of_time_unit:
                    r.insurance_price_unit = insurance_amount / r.sol_id.number_of_time_unit
                else:
                    r.insurance_price_unit = \
                        r.sol_id.rental_qty * insurance_amount / r.sol_id.product_uom_qty

