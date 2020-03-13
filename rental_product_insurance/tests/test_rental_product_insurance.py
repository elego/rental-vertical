# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields


class TestRentalProductInsurance(RentalStockCommon):

    def setUp(self):
        super().setUp()

        # Product Created A
        ProductObj = self.env['product.product']
        self.productA = ProductObj.create(
            {'name': 'Product A', 'type': 'product'})
        # Rental Service (Day) of Product A
        self.rental_service_day = self._create_rental_service_day(
            self.productA)
        self.product_insurance = self.env.ref(
            'rental_product_insurance.product_product_insurance')
        self.date_start = fields.Date.from_string(fields.Date.today())
        self.date_end = self.date_start + relativedelta(days=1)
        self.rental_order = self.env['sale.order'].create({
            'partner_id': self.partnerA.id,
            'order_line': [(0, 0, {
                'product_id': self.rental_service_day.id,
                'name': self.rental_service_day.name,
                'rental_type': 'new_rental',
                'rental_qty': 1.0,
                'price_unit': 100,
                'product_uom': self.rental_service_day.uom_id.id,
                'start_date': self.date_start,
                'end_date': self.date_end,
                'product_uom_qty': 2.0,
            })],
        })

    def test_00_rental_product_insurance_type_product(self):
        self.productA.write({
            'insurance_type': 'product',
            'insurance_percent': 20,
            'standard_price': 1000,
        })
        # test onchange_insurance_product_id
        self.rental_order.order_line.onchange_insurance_product_id()
        self.assertEqual(
            self.rental_order.order_line.insurance_type, 'product')
        self.assertEqual(self.rental_order.order_line.insurance_percent, 20)

        self.rental_order.action_confirm()
        self.assertEqual(len(self.rental_order.order_line), 2)
        check_insurance = False
        for line in self.rental_order.order_line:
            if line.product_id == self.product_insurance:
                self.assertEqual(line.price_unit, 200)
                self.assertEqual(line.name, "Insurance: Rental of Product A (Day)")
                check_insurance = True
        self.assertEqual(check_insurance, True)
        
    def test_01_rental_product_insurance_type_rental(self):
        self.productA.write({
            'insurance_type': 'rental',
            'insurance_percent': 20,
            'standard_price': 1000,
        })
        # test onchange_insurance_product_id
        self.rental_order.order_line.onchange_insurance_product_id()
        self.assertEqual(
            self.rental_order.order_line.insurance_type, 'rental')
        self.assertEqual(self.rental_order.order_line.insurance_percent, 20)

        self.rental_order.action_confirm()
        self.assertEqual(len(self.rental_order.order_line), 2)
        check_insurance = False
        for line in self.rental_order.order_line:
            if line.product_id == self.product_insurance:
                self.assertEqual(line.price_unit, 40)
                check_insurance = True
                self.assertEqual(line.name, "Insurance: Rental of Product A (Day)")
        self.assertEqual(check_insurance, True)
