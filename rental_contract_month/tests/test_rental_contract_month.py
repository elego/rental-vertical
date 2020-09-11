# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon


class TestRentalProductInsurance(RentalStockCommon):

    def setUp(self):
        super().setUp()

        # Product Created A
        ProductObj = self.env['product.product']
        self.productA = ProductObj.create({
            'name': 'Product A',
            'type': 'product',
        })

        self.contract_template = self.env.ref(
            'rental_contract.rental_contract_template')

    def test_00_rental_contract_month(self):
        self.productA.write({
            'rental': True,
            'rental_of_month': True,
            'rental_price_month': 1000,
        })
        product_month = self.productA.product_rental_month_id
        self.assertEqual(
            product_month.is_contract, True)
        self.assertEqual(
            product_month.property_contract_template_id.id,
            self.contract_template.id
        )
