# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields, exceptions


class TestRentalPricelist(RentalStockCommon):

    def setUp(self):
        super().setUp()

        # Product Created A, B, C
        ProductObj = self.env['product.product']
        self.productA = ProductObj.create({
            'name': 'Product A',
            'type': 'product',
            'rental': True,
            'rental_of_day': True,
            'rental_price_day': 200,
            'rental_of_interval': True,
            'rental_price_interval': 1000,
            'rental_interval_max': 21,
        })
        self.today = fields.Date.from_string(fields.Date.today())
        self.date_4_day_later = self.today + relativedelta(days=4)
        self.date_12_day_later = self.today + relativedelta(days=12)
        self.date_17_day_later = self.today + relativedelta(days=17)
        self.date_24_day_later = self.today + relativedelta(days=24)
        self.rental_order = self.env['sale.order'].with_context({
            'default_type_id': self.rental_sale_type.id,
        }).create({
            'partner_id': self.partnerA.id,
            'pricelist_id': self.env.ref('product.list0').id,
        })

    def _run_sol_onchange_display_product_id(self, line):
        line.onchange_display_product_id() # product_id, rental changed
        line.product_id_change()
        line.onchange_rental() # product_id changed again
        line.product_id_change() # product_uom changed
        line.product_uom_change()
        line.rental_product_id_change() # set start end date manually

    def _run_sol_onchange_date(self, line, start_date=False, end_date=False):
        if start_date:
            line.start_date = start_date
        if end_date:
            line.end_date = end_date
        line.onchange_start_end_date() # number_of_time_unit changed
        line.rental_qty_number_of_days_change() # product_uom_qty changed
        line.product_uom_change()

    def test_00_interval_price(self):
        """
            Create Interval Prices for productA
            Activate interval price in sale order line
            Change End Date and rental_qty
            Reset field rental_interval_price
        """
        # Create Interval Prices for productA
        self.env.user.company_id.write({
            'rental_price_interval_rule_ids': [
                (0, 0, {'name': '0-7 interval', 'factor': 1, 'min_quantity': 0}),
                (0, 0, {'name': '8-14 interval', 'factor': 1.75, 'min_quantity': 8}),
                (0, 0, {'name': '15-21 interval', 'factor': 2.25, 'min_quantity': 15}),
            ]
        })
        self.productA.action_reset_rental_price_interval_items()
        check_p1 = check_p2 = check_p3 = False
        for price in self.productA.rental_price_interval_item_ids:
            if price.min_quantity == 0:
                self.assertEqual(price.price, 1000)
                self.assertEqual(price.name, '0-7 interval')
                check_p1 = True
            elif price.min_quantity == 8:
                self.assertEqual(price.price, 1750)
                self.assertEqual(price.name, '8-14 interval')
                check_p2 = True
            elif price.min_quantity == 15:
                self.assertEqual(price.price, 2250)
                self.assertEqual(price.name, '15-21 interval')
                check_p3 = True
        self.assertTrue(check_p1)
        self.assertTrue(check_p2)
        self.assertTrue(check_p3)
        # Activate interval price in sale order line
        line = self.env['sale.order.line'].with_context({
            'type_id': self.rental_sale_type.id,
        }).new({
            'order_id': self.rental_order.id,
            'display_product_id': self.productA.id,
            'start_date': self.today,
            'end_date': self.date_17_day_later,
        })
        self._run_sol_onchange_display_product_id(line)
        self._run_sol_onchange_date(line)
        self.assertEqual(line.rental, True)
        self.assertEqual(line.rental_interval_price, True)
        self.assertEqual(line.rental_type, 'new_rental')
        self.assertEqual(line.can_sell_rental, False)
        self.assertEqual(line.product_id, self.productA.product_rental_day_id)
        self.assertEqual(line.display_product_id, self.productA)
        self.assertEqual(line.product_uom, self.uom_day)
        self.assertEqual(line.product_uom_qty, 1)
        self.assertEqual(line.rental_qty, 1)
        self.assertEqual(line.number_of_time_unit, 18)
        self.assertEqual(line.price_unit, 2250)
        self.assertEqual(line.price_subtotal, 2250)
        self.assertEqual(line.rental_interval_name, '15-21 interval')
        # Change End Date and rental_qty
        line.rental_qty = 2
        self._run_sol_onchange_date(line, end_date=self.date_12_day_later)
        self.assertEqual(line.rental_qty, 2)
        self.assertEqual(line.price_unit, 3500) # 2 * 1750
        self.assertEqual(line.price_subtotal, 3500)
        self.assertEqual(line.rental_interval_name, '8-14 interval')
        # Reset field rental_interval_price
        line.rental_interval_price = False
        line.onchange_rental_interval_price()
        self.assertEqual(line.price_unit, 200)
        line.rental_interval_price = True
        self.assertEqual(line.rental_interval_price, True)
        line.onchange_rental_interval_price()
        self.assertEqual(line.price_unit, 3500) # 2 * 1750
        self._run_sol_onchange_date(line, end_date=self.date_4_day_later)
        self.assertEqual(line.price_unit, 2000) # 2 * 1000
        self.assertEqual(line.price_subtotal, 2000)
        self.assertEqual(line.rental_interval_name, '0-7 interval')
        with self.assertRaises(exceptions.UserError) as e:
            self._run_sol_onchange_date(line, end_date=self.date_24_day_later)
        self.assertEqual(
            'Max rental interval (21 days) is exceeded.',
            e.exception.name
        )

    def test_01_no_found_interval_price(self):
        """
            Activate interval price in sale order line
        """
        line = self.env['sale.order.line'].with_context({
            'type_id': self.rental_sale_type.id,
        }).new({
            'order_id': self.rental_order.id,
            'display_product_id': self.productA.id,
            'start_date': self.today,
            'end_date': self.date_17_day_later,
        })
        with self.assertRaises(exceptions.UserError) as e:
            self._run_sol_onchange_display_product_id(line)
            self._run_sol_onchange_date(line)
        self.assertEqual(
            'No found suitable interval price.',
            e.exception.name
        )
