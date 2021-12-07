# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_routing.tests.test_rental_routing import TestRentalRouting
from odoo import fields, exceptions


class TestRentalForwardShipmentPlan(TestRentalRouting):
    def setUp(self):
        super().setUp()
        self.product_rental.trans_purchase_request = True
        self.service_rental = self._create_rental_service_day(self.product_rental)
        self.product_trans_pr_1 = self.env["product.product"].create(
            {
                "name": "Transport PR 1",
                "type": "service",
                "is_transport": True,
                "transport_service_type": "pr",
            }
        )
        self.incotermsA = self.env["account.incoterms"].create(
            {
                "name": "Incoterm External Shipment",
                "trans_pr_needed": True,
                "code": "ext_shipment",
            }
        )

    def create_shipment_plan(self, rental_order):
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": rental_order.id,
                }
            )
            .create(
                {
                    "service_product_ids": [
                        (
                            4,
                            self.product_trans_pr_1.id,
                        ),
                    ]
                }
            )
        )
        wizard.onchange_service_product_ids()
        shipment_plan, return_shipment_plan = wizard.action_confirm()
        return shipment_plan, return_shipment_plan


    def test_00_rental_forward_shipment_plan(self):
        """
        1. Create Rental Orders (1, 2, 3) for product_rental
        2. Routing: order 1 -> order 2
        3. Forward: order 2 -> order 3
        """
        # 1. Create Rental Orders for product_rental
        rental_order_1 = self._create_rental_order(
            self.partnerA.id, self.date_0101, self.date_0108)
        rental_order_2 = self._create_rental_order(
            self.partnerB.id, self.date_0110, self.date_0117)
        rental_order_3 = self._create_rental_order(
            self.partnerC.id, self.date_0119, self.date_0126)
        rental_order_1.incoterm = self.incotermsA.id
        rental_order_2.incoterm = self.incotermsA.id
        rental_order_3.incoterm = self.incotermsA.id
        # Create shipment plan and delivery order
        shipment_plan_1, return_shipment_plan_1 = self.create_shipment_plan(rental_order_1)
        shipment_plan_2, return_shipment_plan_2 = self.create_shipment_plan(rental_order_2)
        shipment_plan_3, return_shipment_plan_3 = self.create_shipment_plan(rental_order_3)
        rental_order_1.action_confirm()
        rental_order_2.action_confirm()
        rental_2 = self.env["sale.rental"].search(
            [("start_order_line_id", "=", rental_order_2.order_line.id)]
        )
        # 2. Routing: order 1 -> order 2
        wizard = self.env["sale.rental.route"].with_context(
            {
                "active_model": "sale.order.line",
                "active_ids": rental_order_1.order_line.ids,
            }
        ).create({})
        wizard.in_lines.rental_out_id = rental_2
        wizard.in_lines.onchange_rental_out_id()
        wizard.action_confirm()
        # 3. Forward: order 2 -> order 3
        rental_order_3.order_line.can_forward_rental = True
        rental_order_3.order_line.forward_rental_id = rental_2
        rental_order_3.action_confirm()
        rental_order_1._compute_shipment_plans()
        rental_order_2._compute_shipment_plans()
        rental_order_3._compute_shipment_plans()
        self.assertEqual(rental_order_1.trans_shipment_plan_count, 3.0)
        self.assertEqual(rental_order_2.trans_shipment_plan_count, 4.0)
        self.assertEqual(rental_order_3.trans_shipment_plan_count, 3.0)
        # Check Sipment Plans after Changing of Routing
        check_11 = check_12 = check_13 = False
        for sp in rental_order_1.trans_shipment_plan_ids:
            if sp.from_address_id == self.env.user.company_id.partner_id and sp.to_address_id == self.partnerA:
                if sp.location_id == self.warehouse0.rental_in_location_id and sp.location_dest_id == self.partnerA.rental_onsite_location_id:
                    check_11 = True
            if sp.to_address_id == self.env.user.company_id.partner_id and sp.from_address_id == self.partnerA:
                if sp.location_dest_id == self.warehouse0.rental_in_location_id and sp.location_id == self.partnerA.rental_onsite_location_id:
                    check_12 = True
            if sp.from_address_id == self.partnerA and sp.to_address_id == self.partnerB:
                if sp.location_id == self.partnerA.rental_onsite_location_id and sp.location_dest_id == self.partnerB.rental_onsite_location_id:
                    check_13 = True
        check_21 = check_22 = check_23 = check_24 = False
        for sp in rental_order_2.trans_shipment_plan_ids:
            if sp.from_address_id == self.env.user.company_id.partner_id and sp.to_address_id == self.partnerB:
                if sp.location_id == self.warehouse0.rental_in_location_id and sp.location_dest_id == self.partnerB.rental_onsite_location_id:
                    check_21 = True
            if sp.to_address_id == self.env.user.company_id.partner_id and sp.from_address_id == self.partnerB:
                if sp.location_dest_id == self.warehouse0.rental_in_location_id and sp.location_id == self.partnerB.rental_onsite_location_id:
                    check_22 = True
            if sp.from_address_id == self.partnerA and sp.to_address_id == self.partnerB:
                if sp.location_id == self.partnerA.rental_onsite_location_id and sp.location_dest_id == self.partnerB.rental_onsite_location_id:
                    check_23 = True
            if sp.from_address_id == self.partnerB and sp.to_address_id == self.partnerC:
                if sp.location_id == self.partnerB.rental_onsite_location_id and sp.location_dest_id == self.partnerC.rental_onsite_location_id:
                    check_24 = True
        check_31 = check_32 = check_33 = False
        for sp in rental_order_3.trans_shipment_plan_ids:
            if sp.from_address_id == self.env.user.company_id.partner_id and sp.to_address_id == self.partnerC:
                if sp.location_id == self.warehouse0.rental_in_location_id and sp.location_dest_id == self.partnerC.rental_onsite_location_id:
                    check_31 = True
            if sp.to_address_id == self.env.user.company_id.partner_id and sp.from_address_id == self.partnerC:
                if sp.location_dest_id == self.warehouse0.rental_in_location_id and sp.location_id == self.partnerC.rental_onsite_location_id:
                    check_32 = True
            if sp.from_address_id == self.partnerB and sp.to_address_id == self.partnerC:
                if sp.location_id == self.partnerB.rental_onsite_location_id and sp.location_dest_id == self.partnerC.rental_onsite_location_id:
                    check_33 = True
        self.assertTrue(check_11)
        self.assertTrue(check_12)
        self.assertTrue(check_13)
        self.assertTrue(check_21)
        self.assertTrue(check_22)
        self.assertTrue(check_23)
        self.assertTrue(check_24)
        self.assertTrue(check_31)
        self.assertTrue(check_32)
        self.assertTrue(check_33)
