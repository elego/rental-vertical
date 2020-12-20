# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from datetime import date, timedelta

import logging

_logger = logging.getLogger(__name__)


class TestRentalProductSet(TransactionCase):
    """ Test Rental Product set"""

    def setUp(self):
        super(TestRentalProductSet, self).setUp()
        self.sale_order = self.env["sale.order"]
        self.product_set_add = self.env["product.set.add"]
        self.uom_month = self.env.ref("rental_base.product_uom_month")
        self.uom_day = self.env.ref("uom.product_uom_day")
        # create
        # Rental Product1 : rental_of_month=True
        # Rental Product 2 : rental_of_month=True, rental_of_day=True
        rental_product1 = self.env["product.product"].create(
            {
                "name": "RentalProduct_1",
                "default_code": "RP001",
                "type": "product",
                "sale_ok": True,
                "rental": True,
                "rental_of_month": True,
                "rental_price_month": 300.00,
            }
        )
        self.assertEqual(len(rental_product1.rental_service_ids), 1)
        rental_product2 = self.env["product.product"].create(
            {
                "name": "RentalProduct_2",
                "default_code": "RP002",
                "type": "product",
                "sale_ok": True,
                "rental": True,
                "rental_of_month": True,
                "rental_price_month": 300.00,
                "rental_of_day": True,
                "rental_price_day": 200.00,
            }
        )
        self.assertEqual(len(rental_product2.rental_service_ids), 2)
        rental_product2_service_day = rental_product2.product_rental_day_id
        # create
        # Rental Product Set :
        # Set Lines : Rental Product_1(Months),
        #             Rental Product_2(Months,Days)
        self.rental_product_set = self.env["product.set"].create(
            {
                "name": "Rental Product Set",
                "ref": "Rental Product Set",
            }
        )
        product_set_line1 = self.env["product.set.line"].create(
            {
                "product_set_id": self.rental_product_set.id,
                "product_id": rental_product1.id,
                "quantity": 1,
                "discount": 10,
                "sequence": 30,
            }
        )
        product_set_line2 = self.env["product.set.line"].create(
            {
                "product_set_id": self.rental_product_set.id,
                "product_id": rental_product2.id,
                "quantity": 1,
                "discount": 20,
                "sequence": 40,
            }
        )
        # set end_date with fix days=32
        self.start_date = date.today()
        self.end_date = self.start_date + timedelta(days=32)
        self.end_date_two_motnhs = self.start_date + timedelta(days=64)
        # create so with only one sale order line
        self.rental_so_order = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "type_id": self.env.ref("rental_base.rental_sale_type").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "display_product_id": rental_product2.id,
                            "product_id": rental_product2_service_day.id,
                            "name": rental_product2_service_day.name,
                            "rental": True,
                            "rental_type": "new_rental",
                            "rental_qty": 1.0,
                            "product_uom": rental_product2_service_day.uom_id.id,
                            "start_date": self.start_date,
                            "end_date": self.end_date,
                        },
                    )
                ],
            }
        )

        self.sale_order_line = self.rental_so_order.order_line[0]
        self.sale_order_line.onchange_rental()
        self.sale_order_line.rental_product_id_change()
        self.sale_order_line.product_uom_change()
        self.sale_order_line.product_id_change()
        self.sale_order_line.onchange_start_end_date()
        self.sale_order_line.rental_qty_number_of_days_change()

    def test_rental_add_set(self):
        so = self.rental_so_order
        count_lines = len(so.order_line)  # count_lines = 1

        # Open wizard and set rental product set data
        # choose 'Month(s)' as Uom
        # it will add two so lines from product set
        so_set = self.product_set_add.with_context(active_id=so.id).create(
            {
                "product_set_id": self.rental_product_set.id,
                "rental_ok": True,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "quantity": 1,
                "uom_id": self.uom_month.id,
            }
        )
        so_set._onchange_product_set_id()
        so_set.add_set()
        # check sale order (3 = 1 + 2)
        self.assertEqual(len(so.order_line), count_lines + 2)
        # check uom
        self.assertEquals(so.order_line[0].product_uom, self.uom_day)
        self.assertEquals(so.order_line[1].product_uom, self.uom_month)
        self.assertEquals(so.order_line[2].product_uom, self.uom_month)
        # check rental_type = 'new_rental'
        self.assertEquals(
            so.order_line.mapped("rental_type"),
            ["new_rental", "new_rental", "new_rental"],
        )
        # check rental = True
        self.assertEquals(so.order_line.mapped("rental"), [True, True, True])
        # check start_date
        self.assertEquals(
            so.order_line.mapped("start_date"),
            [self.start_date, self.start_date, self.start_date],
        )
        # check end_date
        self.assertEquals(
            so.order_line.mapped("end_date"),
            [self.end_date, self.end_date, self.end_date],
        )
        # check product_uom_qty, rental_qty
        self.assertEquals(so.order_line.mapped("product_uom_qty"), [33.0, 1.0, 1.0])
        self.assertEquals(so.order_line.mapped("rental_qty"), [1.0, 1.0, 1.0])

    def test_rental_add_set_on_empty_so(self):
        # create so without sale order line
        so = self.sale_order.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "type_id": self.env.ref("rental_base.rental_sale_type").id,
            }
        )
        # Open wizard and set rental product set data
        # choose 'Month(s)' as Uom
        # it will add two so lines from product set
        so_set = self.product_set_add.with_context(active_id=so.id).create(
            {
                "product_set_id": self.rental_product_set.id,
                "rental_ok": True,
                "start_date": self.start_date,
                "end_date": self.end_date_two_motnhs,
                "quantity": 1,
                "uom_id": self.uom_month.id,
            }
        )
        so_set._onchange_product_set_id()
        so_set.add_set()
        # check sale order
        self.assertEqual(len(so.order_line), 2)
        # check uom
        self.assertEquals(so.order_line[0].product_uom, self.uom_month)
        self.assertEquals(so.order_line[1].product_uom, self.uom_month)

        # check rental_type = 'new_rental'
        self.assertEquals(
            so.order_line.mapped("rental_type"), ["new_rental", "new_rental"]
        )
        # check rental = True
        self.assertEquals(so.order_line.mapped("rental"), [True, True])
        # check start_date
        self.assertEquals(
            so.order_line.mapped("start_date"), [self.start_date, self.start_date]
        )
        # check end_date
        self.assertEquals(
            so.order_line.mapped("end_date"),
            [self.end_date_two_motnhs, self.end_date_two_motnhs],
        )
        # check product_uom_qty, rental_qty
        self.assertEquals(so.order_line.mapped("product_uom_qty"), [2.0, 2.0])
        self.assertEquals(so.order_line.mapped("rental_qty"), [1.0, 1.0])
