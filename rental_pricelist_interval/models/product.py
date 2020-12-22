# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class RentalPriceIntervalItem(models.Model):
    _name = 'rental.price.interval.item'
    _description = 'Rental Price Interval Item'

    name = fields.Char(
        'Name',
    )

    price = fields.Float(
        'Price',
    )

    min_quantity = fields.Integer(
        'Interval (days)',
    )

    product_id = fields.Many2one(
        'product.product',
        'Product'
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    rental_of_interval = fields.Boolean(
        'Rented in interval',
        copy=False,
    )

    rental_interval_max = fields.Integer(
        'Interval days (Max)',
        copy=False,
    )

    rental_price_interval = fields.Float(
        string='Interval Price',
    )

    rental_price_interval_item_ids = fields.One2many(
        'rental.price.interval.item',
        'product_id',
        string='Interval Scale Pricelist Items',
        copy=False,
    )

    @api.multi
    def action_reset_rental_price_interval_items(self):
        self.ensure_one()
        company = self.company_id or self.env.user.company_id
        self.rental_price_interval_item_ids.unlink()
        values = []
        for rule in company.rental_price_interval_rule_ids:
            values.append((0, 0, {
                'name': rule.name,
                'price': self.rental_price_interval * rule.factor,
                'min_quantity': rule.min_quantity
            }))
        self.rental_price_interval_item_ids = values
