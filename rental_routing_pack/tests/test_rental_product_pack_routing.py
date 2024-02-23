# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields


class TestRentalProductPackRouting(RentalStockCommon):
    def setUp(self):
        super().setUp()

        # Product Created A, B, C
        ProductObj = self.env["product.product"]
        self.product = ProductObj.create({"name": "Product ", "type": "product"})
        self.productA = ProductObj.create({"name": "Product A", "type": "product"})
        self.productB = ProductObj.create({"name": "Product B", "type": "product"})
        self.productC = ProductObj.create({"name": "Product C", "type": "product"})
        self.product.write(
            {
                "pack_ok": True,
                "pack_type": "non_detailed",
                "pack_line_ids": [
                    (0, 0, {"product_id": self.productA.id, "quantity": 1}),
                    (0, 0, {"product_id": self.productB.id, "quantity": 1}),
                    (0, 0, {"product_id": self.productC.id, "quantity": 2}),
                ],
            }
        )
        # Rental Service (Day) of Product A
        self.rental_service_day = self._create_rental_service_day(self.product)

        self.date_start = fields.Date.from_string(fields.Date.today())
        self.date_end = self.date_start + relativedelta(days=1)

        self.date_start_2 = self.date_start + relativedelta(days=3)
        self.date_end_2 = self.date_start + relativedelta(days=4)


        self.rental_order_1 = self.env["sale.order"].create(
            {
                "partner_id": self.partnerA.id,
                "partner_shipping_id": self.partnerA.id,
                "type_id": self.rental_sale_type.id,
                "warehouse_id": self.warehouse0.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.rental_service_day.id,
                            "name": self.rental_service_day.name,
                            "rental_type": "new_rental",
                            "rental_qty": 3.0,
                            "product_uom": self.rental_service_day.uom_id.id,
                            "start_date": self.date_start,
                            "end_date": self.date_end,
                            "product_uom_qty": 6.0,
                        },
                    )
                ],
            }
        )

        self.rental_order_2 = self.env["sale.order"].create(
            {
                "partner_id": self.partnerA.id,
                "partner_shipping_id": self.partnerA.id,
                "type_id": self.rental_sale_type.id,
                "warehouse_id": self.warehouse0.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.rental_service_day.id,
                            "name": self.rental_service_day.name,
                            "rental_type": "new_rental",
                            "rental_qty": 2.0,
                            "product_uom": self.rental_service_day.uom_id.id,
                            "start_date": self.date_start_2,
                            "end_date": self.date_end_2,
                            "product_uom_qty": 4.0,
                        },
                    )
                ],
            }
        )

    def _check_unchanged_rental_stock_product_line(self):
        check_1 = check_2 = check_3 = check_4 = check_5 = check_6 = False
        for line in self.rental_order_1.rental_stock_product_line_ids:
            line._compute_total_qty()
            if line.product_id == self.productA:
                self.assertEqual(line.product_qty_out, 3)
                self.assertEqual(line.product_qty_in, 3)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 3)
                self.assertEqual(line.total_qty_in, 3)
                check_1 = True
            if line.product_id == self.productB:
                self.assertEqual(line.product_qty_out, 3)
                self.assertEqual(line.product_qty_in, 3)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 3)
                self.assertEqual(line.total_qty_in, 3)
                check_2 = True
            if line.product_id == self.productC:
                self.assertEqual(line.product_qty_out, 6)
                self.assertEqual(line.product_qty_in, 6)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 6)
                self.assertEqual(line.total_qty_in, 6)
                check_3 = True
        for line in self.rental_order_2.rental_stock_product_line_ids:
            line._compute_total_qty()
            if line.product_id == self.productA:
                self.assertEqual(line.product_qty_out, 2)
                self.assertEqual(line.product_qty_in, 2)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 2)
                self.assertEqual(line.total_qty_in, 2)
                check_4 = True
            if line.product_id == self.productB:
                self.assertEqual(line.product_qty_out, 2)
                self.assertEqual(line.product_qty_in, 2)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 2)
                self.assertEqual(line.total_qty_in, 2)
                check_5 = True
            if line.product_id == self.productC:
                self.assertEqual(line.product_qty_out, 4)
                self.assertEqual(line.product_qty_in, 4)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 4)
                self.assertEqual(line.total_qty_in, 4)
                check_6 = True
        self.assertTrue(check_1 and check_2 and check_3 and check_4 and check_5 and check_6)

    def test_00_rental_product_pack_routing(self):
        self.rental_order_1.action_confirm()
        self.rental_order_2.action_confirm()
        self.assertEqual(len(self.rental_order_1.picking_ids), 2)
        self.assertEqual(len(self.rental_order_2.picking_ids), 2)
        # 1. Check origin stock product line (before Routing)
        self.assertEqual(len(self.rental_order_1.rental_stock_product_line_ids), 3) # A: 3, B: 3, C: 6
        self.assertEqual(len(self.rental_order_2.rental_stock_product_line_ids), 3) # A: 2, B: 2, C: 4
        self._check_unchanged_rental_stock_product_line()

        # 2. Create Wizard for Routing
        wizard = self.env["rental.pack.product.route"].with_context(
            {
                "active_model": "sale.order",
                "active_id": self.rental_order_2.id,
            }
        ).create({})
        wizard.source_order_id = self.rental_order_1
        values = wizard.onchange_source_order_id()["value"]
        
        wizard.write(values)
        self.assertEqual(len(wizard.lines), 3)
        for line in wizard.lines:
            if line.product_id == self.productA:
                line.qty = 1 #take less than required
            if line.product_id == self.productB:
                line.qty = 2 #take same as required
            if line.product_id == self.productC:
                line.qty = 6 #take more than required
        wizard.action_confirm()

        # 3. Check origin stock product line again (after Routint)
        check_1 = check_2 = check_3 = check_4 = check_5 = check_6 = False
        for line in self.rental_order_1.rental_stock_product_line_ids:
            line._compute_total_qty()
            if line.product_id == self.productA:
                self.assertEqual(line.product_qty_out, 3)
                self.assertEqual(line.product_qty_in, 3)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 1)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 1)
                self.assertEqual(line.total_qty_out, 3)
                self.assertEqual(line.total_qty_in, 3)
                self.assertEqual(line.out_move_id.product_qty, 3)
                self.assertEqual(line.in_move_id.product_qty, 2)
                check_1 = True
            if line.product_id == self.productB:
                self.assertEqual(line.product_qty_out, 3)
                self.assertEqual(line.product_qty_in, 3)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 2)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 2)
                self.assertEqual(line.total_qty_out, 3)
                self.assertEqual(line.total_qty_in, 3)
                self.assertEqual(line.out_move_id.product_qty, 3)
                self.assertEqual(line.in_move_id.product_qty, 1)
                check_2 = True
            if line.product_id == self.productC:
                self.assertEqual(line.product_qty_out, 6)
                self.assertEqual(line.product_qty_in, 6)
                self.assertEqual(line.routed_qty_out, 0)
                self.assertEqual(line.routed_qty_in, 6)
                self.assertEqual(line.reduced_qty_out, 0)
                self.assertEqual(line.reduced_qty_in, 6)
                self.assertEqual(line.total_qty_out, 6)
                self.assertEqual(line.total_qty_in, 6)
                self.assertEqual(line.out_move_id.product_qty, 6)
                self.assertEqual(line.in_move_id.product_qty, 0)
                check_3 = True
        for line in self.rental_order_2.rental_stock_product_line_ids:
            line._compute_total_qty()
            if line.product_id == self.productA:
                self.assertEqual(line.product_qty_out, 2)
                self.assertEqual(line.product_qty_in, 2)
                self.assertEqual(line.routed_qty_out, 1)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 1)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 2)
                self.assertEqual(line.total_qty_in, 2)
                self.assertEqual(line.out_move_id.product_qty, 1)
                self.assertEqual(line.in_move_id.product_qty, 2)
                check_4 = True
            if line.product_id == self.productB:
                self.assertEqual(line.product_qty_out, 2)
                self.assertEqual(line.product_qty_in, 2)
                self.assertEqual(line.routed_qty_out, 2)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 2)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 2)
                self.assertEqual(line.total_qty_in, 2)
                self.assertEqual(line.out_move_id.product_qty, 0)
                self.assertEqual(line.in_move_id.product_qty, 2)
                check_5 = True
            if line.product_id == self.productC:
                self.assertEqual(line.product_qty_out, 4)
                self.assertEqual(line.product_qty_in, 4)
                self.assertEqual(line.routed_qty_out, 6)
                self.assertEqual(line.routed_qty_in, 0)
                self.assertEqual(line.reduced_qty_out, 4)
                self.assertEqual(line.reduced_qty_in, 0)
                self.assertEqual(line.total_qty_out, 6)
                self.assertEqual(line.total_qty_in, 6)
                self.assertEqual(line.out_move_id.product_qty, 0)
                self.assertEqual(line.in_move_id.product_qty, 6)
                check_6 = True
        self.assertTrue(check_1 and check_2 and check_3 and check_4 and check_5 and check_6)
        # 4. Cancel the Routing
        picking_route = self.env["stock.picking"].search(
            [("origin", "=", "%s -> %s" %(self.rental_order_1.name, self.rental_order_2.name))]
        )
        picking_route.action_cancel()
        # 5. Check stock product line (After Cancel of Routing)
        self._check_unchanged_rental_stock_product_line()
