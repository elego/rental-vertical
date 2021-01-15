# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields


class TestRentalProductInstanceState(RentalStockCommon):
    def setUp(self):
        super().setUp()

        # Product A Created
        self.ProductObj = self.env["product.product"]
        self.productA = self.ProductObj.create({"name": "Product A", "type": "product"})
        self.productB = self.ProductObj.create({"name": "Product B", "type": "product"})
        self.productC = self.ProductObj.create({"name": "Product C", "type": "product"})
        self.date_start = fields.Date.from_string(fields.Date.today())
        self.date_end = self.date_start + relativedelta(days=1)

    def test_01_instance_state(self):
        # check function _compute_instance_state
        self.productA.write(
            {
                "product_instance": True,
                "product_timeline_ids": [
                    (
                        0,
                        0,
                        {
                            "order_name": "Dummy",
                            "res_model": "sale.order",
                            "res_id": 1,
                            "click_res_model": "sale.order",
                            "click_res_id": 1,
                            "date_start": self.date_start,
                            "date_end": self.date_end,
                            "product_id": self.productA.id,
                            "type": "reserved",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "order_name": "Dummy",
                            "res_model": "sale.order",
                            "res_id": 1,
                            "click_res_model": "sale.order",
                            "click_res_id": 1,
                            "date_start": self.date_start,
                            "date_end": self.date_end,
                            "product_id": self.productA.id,
                            "type": "rental",
                        },
                    ),
                ],
            }
        )
        self.assertEqual(self.productA.instance_state, "rental")
        self.productB.write(
            {
                "product_instance": True,
                "product_timeline_ids": [
                    (
                        0,
                        0,
                        {
                            "order_name": "Dummy",
                            "res_model": "sale.order",
                            "res_id": 1,
                            "click_res_model": "sale.order",
                            "click_res_id": 1,
                            "date_start": self.date_start,
                            "date_end": self.date_end,
                            "product_id": self.productA.id,
                            "type": "reserved",
                        },
                    ),
                ],
            }
        )
        self.assertEqual(self.productB.instance_state, "reserved")
        self.assertEqual(self.productC.instance_state, "available")

        # check function _search_instance_state
        res = self.ProductObj.search([('instance_state', '=', 'available')])
        self.assertTrue(self.productA not in res)
        self.assertTrue(self.productB not in res)
        self.assertTrue(self.productC in res)
        res = self.ProductObj.search([('instance_state', '=', 'reserved')])
        self.assertTrue(self.productA not in res)
        self.assertTrue(self.productB in res)
        self.assertTrue(self.productC not in res)
        res = self.ProductObj.search([('instance_state', '=', 'rental')])
        self.assertTrue(self.productA in res)
        self.assertTrue(self.productB not in res)
        self.assertTrue(self.productC not in res)

