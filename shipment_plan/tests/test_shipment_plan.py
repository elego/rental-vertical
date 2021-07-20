# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.shipment_plan.tests.common import ShipmentPlanCommon
from odoo import fields, exceptions


class TestShipmentPlan(ShipmentPlanCommon):
    def setUp(self):
        super().setUp()
        # Create Shipment Plan
        self.shipment_plan = self.env["shipment.plan"].create(
            {
                "initial_etd": self.today,
                "initial_eta": self.date_one_month_later,
                "name": "Shipment Plan Test",
                "state": "draft",
                "from_address_id": self.from_address.id,
                "to_address_id": self.to_address.id,
                "note": "This is a Test.",
            }
        )

    def test_00_shipment_plan(self):
        """
        Create PO and PR
        Check PO and PR
        """
        PurchaseObj = self.env["purchase.order"]
        self.shipment_plan.action_confirm()
        self.assertEqual(self.shipment_plan.state, "confirmed")
        self.shipment_plan.action_cancel_draft()
        self.assertEqual(self.shipment_plan.state, "draft")
        self.shipment_plan.action_confirm()
        # Create PR
        wizard = (
            self.env["create.trans.request"]
            .with_context(
                {
                    "active_id": self.shipment_plan.id,
                    "active_model": "shipment.plan",
                }
            )
            .create(
                {
                    "service_product_ids": [
                        (
                            4,
                            self.product_trans_pr_1.id,
                        ),
                        (
                            4,
                            self.product_trans_pr_2.id,
                        ),
                    ]
                }
            )
        )
        wizard.onchange_service_product_ids()
        wizard.action_confirm()
        # Create PO
        wizard = (
            self.env["create.trans.request"]
            .with_context(
                {
                    "active_id": self.shipment_plan.id,
                    "active_model": "shipment.plan",
                }
            )
            .create(
                {
                    "service_product_ids": [
                        (
                            4,
                            self.product_trans_po_1.id,
                        ),
                        (
                            4,
                            self.product_trans_po_2.id,
                        ),
                    ]
                }
            )
        )
        wizard.onchange_service_product_ids()
        wizard.action_confirm()
        # Check PO and PR
        self.assertEqual(self.shipment_plan.trans_po_count, 2)
        self.assertEqual(self.shipment_plan.trans_pr_count, 2)

        po_A = self.shipment_plan.trans_po_ids[0]
        po_B = self.shipment_plan.trans_po_ids[1]

        self.shipment_plan.trans_po_ids[0].action_transport_confirm()
        self.assertTrue(self.shipment_plan.trans_po_ids[0].selected_in_order)
        self.shipment_plan.trans_po_ids[1].action_transport_confirm()
        self.assertTrue(self.shipment_plan.trans_po_ids[1].selected_in_order)
        pr_1 = self.shipment_plan.trans_pr_ids[0]
        pr_1.action_in_progress()
        # create po_1 from pr_1
        po_1 = PurchaseObj.with_context({"default_requisition_id": pr_1.id}).create(
            {"partner_id": self.partnerA.id}
        )
        po_1._onchange_requisition_id()
        # create po_2 and po_3 from pr_2
        pr_2 = self.shipment_plan.trans_pr_ids[1]
        pr_2.action_in_progress()
        po_2 = PurchaseObj.with_context({"default_requisition_id": pr_2.id}).create(
            {"partner_id": self.partnerA.id}
        )
        po_2._onchange_requisition_id()
        po_3 = PurchaseObj.with_context({"default_requisition_id": pr_2.id}).create(
            {"partner_id": self.partnerB.id}
        )
        po_3._onchange_requisition_id()
        # only one po can be confirmed
        po_2.action_transport_confirm()
        with self.assertRaises(exceptions.UserError) as e:
            po_3.action_transport_confirm()
        po_2.button_confirm()
        self.assertEqual(po_2.state, "purchase")
        self.shipment_plan.action_done()
        self.assertEqual(self.shipment_plan.state, "done")
        self.shipment_plan.action_cancel()
        self.assertEqual(self.shipment_plan.state, "cancel")
        self.assertEqual(self.shipment_plan.trans_po_count, 5)
        self.assertEqual(self.shipment_plan.trans_pr_count, 2)
        self.assertTrue(
            all(o.state == "cancel" for o in self.shipment_plan.trans_po_ids)
        )
        self.assertTrue(
            all(o.state == "cancel" for o in self.shipment_plan.trans_pr_ids)
        )
        # Test Smartbutton
        self.shipment_plan.action_view_trans_prs()
        self.shipment_plan.action_view_trans_pos()
