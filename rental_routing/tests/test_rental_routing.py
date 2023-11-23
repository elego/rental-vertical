# Part of rental-vertical See LICENSE file for full copyright and licensing details.


from odoo import fields

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon


class TestRentalRouting(RentalStockCommon):
    def setUp(self):
        super().setUp()
        self.partnerA = self.PartnerObj.create(
            {
                "name": "Partner A",
                "customer_rank": 1,
            }
        )
        self.partnerB = self.PartnerObj.create(
            {
                "name": "Partner B",
                "customer_rank": 1,
            }
        )
        self.partnerC = self.PartnerObj.create(
            {
                "name": "Partner C",
                "customer_rank": 1,
            }
        )
        # Create Product (need Trans PR) for Sale
        ProductObj = self.env["product.product"]
        self.product_rental = ProductObj.create(
            {
                "name": "Product for Rental",
                "type": "product",
                "categ_id": self.category_all.id,
                #    "trans_purchase_request": True, # FIXME: This is a customer-specific extension!
            }
        )
        self.service_rental = self._create_rental_service_day(self.product_rental)
        self.date_0101 = fields.Date.from_string("2021-01-01")
        self.date_0108 = fields.Date.from_string("2021-01-08")
        self.date_0110 = fields.Date.from_string("2021-01-10")
        self.date_0117 = fields.Date.from_string("2021-01-17")
        self.date_0119 = fields.Date.from_string("2021-01-19")
        self.date_0126 = fields.Date.from_string("2021-01-26")

    def test_00_rental_routing(self):
        """
        1. Create Rental Orders (1, 2, 3) for product_rental
        2. Routing: order 1 -> order 2
        3. Forward: order 2 -> order 3
        """
        # 1. Create Rental Orders for product_rental
        rental_order_1 = self._create_rental_order(
            self.partnerA.id, self.date_0101, self.date_0108
        )
        rental_order_2 = self._create_rental_order(
            self.partnerB.id, self.date_0110, self.date_0117
        )
        rental_order_3 = self._create_rental_order(
            self.partnerC.id, self.date_0119, self.date_0126
        )
        rental_order_1.action_confirm()
        rental_order_2.action_confirm()
        self.assertEqual(rental_order_1.delivery_count, 2)
        self.assertEqual(rental_order_2.delivery_count, 2)
        self.assertEqual(rental_order_3.delivery_count, 0)
        rental_2 = self.env["sale.rental"].search(
            [("start_order_line_id", "=", rental_order_2.order_line.id)]
        )
        # 2. Routing: order 1 -> order 2
        wizard = (
            self.env["sale.rental.route"]
            .with_context(
                {
                    "active_model": "sale.order.line",
                    "active_ids": rental_order_1.order_line.ids,
                }
            )
            .create({})
        )
        wizard.in_lines.rental_out_id = rental_2
        wizard.in_lines.onchange_rental_out_id()
        wizard.action_confirm()
        self.assertEqual(rental_order_1.delivery_count, 3)
        self.assertEqual(rental_order_2.delivery_count, 3)
        # 3. Forward: order 2 -> order 3
        rental_order_3.order_line.can_forward_rental = True
        rental_order_3.order_line.forward_rental_id = rental_2
        rental_order_3.action_confirm()
        self.assertEqual(rental_order_2.delivery_count, 4)
        self.assertEqual(rental_order_3.delivery_count, 3)
        PickingObj = self.env["stock.picking"]
        # check Pickings of order 1
        check_11 = check_12 = check_13 = False
        for picking in PickingObj.browse(
            rental_order_1._get_all_picking_ids()[rental_order_1.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerA.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_11 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.partnerB.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_12 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_13 = True
        self.assertTrue(check_11)  # origin picking out
        self.assertTrue(check_12)  # new picking in
        self.assertTrue(check_13)  # origin picking in
        # check Pickings of order 2
        check_21 = check_22 = check_23 = check_24 = False
        for picking in PickingObj.browse(
            rental_order_2._get_all_picking_ids()[rental_order_2.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerB.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_21 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_22 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.partnerB.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_23 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_24 = True
        self.assertTrue(check_21)  # origin picking out
        self.assertTrue(check_22)  # origin picking in
        self.assertTrue(check_23)  # new picking out
        self.assertTrue(check_24)  # new picking in
        # check Pickings of order 3
        check_31 = check_32 = check_33 = False
        for picking in PickingObj.browse(
            rental_order_3._get_all_picking_ids()[rental_order_3.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_31 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_32 = True
            if (
                picking.location_id == self.partnerC.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_33 = True
        self.assertTrue(check_31)  # origin picking out
        self.assertTrue(check_32)  # new picking out
        self.assertTrue(check_33)  # origin picking in

    def test_01_rental_routing_qty(self):
        """
        1. Create Rental Orders (1, 2, 3) for product_rental
        2. Routing: order 1 -> order 3 (qty 1)
        3. Routing: order 2 -> order 3 (qty 2)
        """
        # 1. Create Rental Orders for product_rental
        rental_order_1 = self._create_rental_order(
            self.partnerA.id, self.date_0101, self.date_0108, qty=1
        )
        rental_order_2 = self._create_rental_order(
            self.partnerB.id, self.date_0110, self.date_0117, qty=3
        )
        rental_order_3 = self._create_rental_order(
            self.partnerC.id, self.date_0119, self.date_0126, qty=3
        )
        rental_order_1.action_confirm()
        rental_order_2.action_confirm()
        rental_order_3.action_confirm()
        rental_1 = self.env["sale.rental"].search(
            [("start_order_line_id", "=", rental_order_1.order_line.id)]
        )
        rental_2 = self.env["sale.rental"].search(
            [("start_order_line_id", "=", rental_order_2.order_line.id)]
        )
        rental_3 = self.env["sale.rental"].search(
            [("start_order_line_id", "=", rental_order_3.order_line.id)]
        )

        # 2. Routing: order 1 -> order 3
        wizard = (
            self.env["sale.rental.route"]
            .with_context(
                {
                    "active_model": "sale.order.line",
                    "active_ids": rental_order_1.order_line.ids,
                }
            )
            .create({})
        )
        wizard.in_lines.rental_out_id = rental_3
        wizard.in_lines.onchange_rental_out_id()
        # print(wizard.in_lines.rental_id)
        # print(wizard.in_lines.move_id)
        self.assertEqual(wizard.in_lines.qty, 1.0)
        self.assertEqual(wizard.in_lines.rental_avail_qty, 3.0)
        # print(wizard.in_lines.rental_out_id)
        # print(wizard.in_lines.rental_out_move_id)
        self.assertEqual(wizard.in_lines.rental_end_date, self.date_0108)
        # print(wizard.in_lines.rental_onsite_location_id)
        wizard.action_confirm()

        # 3. Routing: order 2 -> order 3
        wizard = (
            self.env["sale.rental.route"]
            .with_context(
                {
                    "active_model": "sale.order.line",
                    "active_ids": rental_order_3.order_line.ids,
                }
            )
            .create({})
        )
        wizard.out_lines.rental_in_id = rental_2
        wizard.out_lines.onchange_rental_in_id()
        # print(wizard.out_lines.rental_id)
        # print(wizard.out_lines.move_id)
        self.assertEqual(wizard.out_lines.qty, 2.0)
        self.assertEqual(wizard.out_lines.rental_avail_qty, 3.0)
        # print(wizard.out_lines.rental_in_id)
        # print(wizard.out_lines.rental_in_move_id)
        self.assertEqual(wizard.out_lines.rental_start_date, self.date_0119)
        # print(wizard.out_lines.rental_onsite_location_id)
        wizard.action_confirm()

        PickingObj = self.env["stock.picking"]
        # check Pickings of order 1
        check_11 = check_12 = check_13 = False
        for picking in PickingObj.browse(
            rental_order_1._get_all_picking_ids()[rental_order_1.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerA.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_11 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_12 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_13 = True
        self.assertTrue(check_11)  # origin picking out
        self.assertTrue(check_12)  # new picking in
        self.assertTrue(check_13)  # origin picking in
        # check Pickings of order 2
        check_21 = check_22 = check_23 = False
        for picking in PickingObj.browse(
            rental_order_2._get_all_picking_ids()[rental_order_2.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerB.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 3
            ):
                check_21 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_22 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 2
            ):
                check_23 = True
        self.assertTrue(check_21)  # origin picking out
        self.assertTrue(check_22)  # origin picking in
        self.assertTrue(check_23)  # new picking in
        # check Pickings of order 3
        check_31 = check_32 = check_33 = False
        for picking in PickingObj.browse(
            rental_order_3._get_all_picking_ids()[rental_order_3.id]
        ):
            if (
                picking.location_id == self.warehouse0.rental_in_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 0
            ):
                check_31 = True
            if (
                picking.location_id == self.partnerA.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 1
            ):
                check_32 = True
            if (
                picking.location_id == self.partnerB.rental_onsite_location_id
                and picking.location_dest_id == self.partnerC.rental_onsite_location_id
                and picking.move_lines[0].product_uom_qty == 2
            ):
                check_33 = True
            if (
                picking.location_id == self.partnerC.rental_onsite_location_id
                and picking.location_dest_id == self.warehouse0.rental_in_location_id
                and picking.move_lines[0].product_uom_qty == 3
            ):
                check_34 = True
        self.assertTrue(check_31)  # origin picking out
        self.assertTrue(check_32)  # new picking out (qty 1)
        self.assertTrue(check_33)  # new picking out (qty 2)
        self.assertTrue(check_34)  # origin picking in
