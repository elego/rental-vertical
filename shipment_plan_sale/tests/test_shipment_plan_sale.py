# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.shipment_plan.tests.common import ShipmentPlanCommon
from odoo import fields, exceptions


def confirm_shipment_plan_pos(self, shipment_plan):
    # Confirm all origin POs
    for po in shipment_plan.trans_po_ids:
        po.action_transport_confirm()
    # Create POs (po_1 und po_2) from PR
    for pr in shipment_plan.trans_pr_ids:
        pr.action_in_progress()
        pr.line_ids.price_unit = 330
        po_1 = self.PurchaseObj.new(
            {"partner_id": self.partnerA.id, "requisition_id": pr.id}
        )
        po_1._onchange_requisition_id()
        vals = po_1._convert_to_write(po_1._cache)
        po_1 = self.env["purchase.order"].create(vals)
        po_2 = self.PurchaseObj.new(
            {"partner_id": self.partnerB.id, "requisition_id": pr.id}
        )
        po_2._onchange_requisition_id()
        vals = po_2._convert_to_write(po_2._cache)
        po_2 = self.env["purchase.order"].create(vals)
        # Confirm only po_2
        po_2.action_transport_confirm()


class TestShipmentPlanSale(ShipmentPlanCommon):
    def setUp(self):
        super().setUp()
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.customer_location = self.env.ref("stock.stock_location_customers")
        self.incotermsA = self.env["account.incoterms"].create(
            {
                "name": "Incoterm External Shipment",
                "trans_pr_needed": True,
                "code": "ext_shipment",
            }
        )
        self.PurchaseObj = self.env["purchase.order"]
        # Create Product (need Trans PR) for Sale
        ProductObj = self.env["product.product"]
        self.product_sale = ProductObj.create(
            {
                "name": "Product for Sale",
                "type": "product",
                "trans_purchase_request": True,
            }
        )

    def _create_sale_order(self):
        """
        Create a Sale Order with Product (self.product_sale)
        """
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partnerC.id,
                "partner_invoice_id": self.partnerC.id,
                "partner_shipping_id": self.partnerC.id,
                "incoterm": self.incotermsA.id,
                "pricelist_id": self.env.ref("product.list0").id,
                "picking_policy": "direct",
                "warehouse_id": self.env.ref("stock.warehouse0").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "Product for Sale",
                            "product_id": self.product_sale.id,
                            "product_uom_qty": 1,
                            "price_unit": 10000,
                            "product_uom": self.uom_unit.id,
                        },
                    )
                ],
            }
        )
        self.assertEqual(sale_order.state, "draft")
        return sale_order

    def test_00_shipment_plan_sale_multi_cost(self):
        """
        1. Set Product for Transport Cost
        2. Create SO for product_sale
        3. Run wizard create.sale.trans.request:
            To Create PO, PR and Shipment Plan
        4. Create PO from PR and Confirm all POs
        5. Run action_create_trans_cost
            To Create SOL for Transport Cost
        6. action_cancel
        """
        # TODO Check Problem after execute the config on picking will be created after confriming the sale order
        # Set cost type 'multi'
        # config = self.env['res.config.settings'].create({
        #    'transport_cost_type': 'multi',
        # })
        # config.execute()
        sale_order = self._create_sale_order()
        sale_order.transport_cost_type = "multi"
        self.assertTrue(sale_order.trans_pr_needed)
        self.assertEqual(sale_order.transport_cost_type, "multi")
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
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
        shipment_plan = wizard.action_confirm()
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
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
        shipment_plan = wizard.action_confirm()
        self.assertEqual(shipment_plan.trans_po_count, 2)
        self.assertEqual(shipment_plan.trans_pr_count, 1)
        self.assertEqual(shipment_plan.location_id, self.stock_location)
        self.assertEqual(shipment_plan.location_dest_id, self.customer_location)
        confirm_shipment_plan_pos(self, shipment_plan)
        # TODO Check why the field 'trans_shipment_plan_id' of
        # sale order line was not set.
        self.assertEqual(sale_order.order_line, shipment_plan.origin_sale_line_ids)
        # print(shipment_plan.origin_sale_line_ids)
        # print(sale_order.order_line)
        # print(sale_order.order_line.trans_shipment_plan_id)
        # It works correctly, if we do this in Web Client.
        # So I have to set it here manually
        sale_order.order_line.trans_shipment_plan_id = shipment_plan
        # There are 4 POs, 3 of them are confirmed
        self.assertEqual(sale_order.trans_shipment_plan_count, 1)
        self.assertEqual(sale_order.trans_pr_count, 1)
        self.assertEqual(shipment_plan.trans_po_count, 4)
        self.assertEqual(sale_order.trans_po_count, 4)
        # Create Transport Cost in Sale Order Line
        sale_order.action_create_trans_cost()
        # 3 lines for transport cost, 1 line for product_sale
        self.assertEqual(len(sale_order.order_line), 4)
        check_prod_po_1 = False
        check_prod_po_2 = False
        check_prod_pr_1 = False
        for line in sale_order.order_line:
            if line.product_id.id == self.product_trans_po_1.id:
                self.assertEqual(line.price_unit, 100)
                check_prod_po_1 = True
            if line.product_id.id == self.product_trans_po_2.id:
                self.assertEqual(line.price_unit, 200)
                check_prod_po_2 = True
            if line.product_id.id == self.product_trans_pr_1.id:
                self.assertEqual(line.price_unit, 330)
                check_prod_pr_1 = True
        self.assertTrue(check_prod_po_1)
        self.assertTrue(check_prod_po_2)
        self.assertTrue(check_prod_pr_1)
        # Test Smartbutton
        sale_order.action_view_trans_prs()
        sale_order.action_view_trans_pos()
        sale_order.action_view_shipment_plans()
        # Confirm Sale Order
        sale_order.action_confirm()
        self.assertEqual(len(sale_order.picking_ids), 1)
        self.assertEqual(
            sale_order.picking_ids[0].shipment_plan_id.id, shipment_plan.id
        )

    def test_01_shipment_plan_sale_single_cost(self):
        """
        1. Change Config with Single Cost ans Set Product for Transport Cost
        2. Create SO for product_sale
        3. Run wizard create.sale.trans.request:
            To Create PO, PR and Shipment Plan
        4. Confirm the 2 POs
        5. Run action_create_trans_cost
            To Create SOL for Transport Cost
        6. Confirm Sale Order
        """
        # Set cost type 'single' and cost product
        config = self.env["res.config.settings"].create(
            {
                "transport_cost_type": "single",
                "transport_cost_product_id": self.product_cost.id,
            }
        )
        config.execute()
        sale_order = self._create_sale_order()
        self.assertEqual(sale_order.transport_cost_type, "single")
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
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
        shipment_plan = wizard.action_confirm()
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
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
        shipment_plan = wizard.action_confirm()
        self.assertEqual(shipment_plan.trans_po_count, 2)
        self.assertEqual(shipment_plan.trans_pr_count, 1)
        confirm_shipment_plan_pos(self, shipment_plan)
        # TODO Check why the field 'trans_shipment_plan_id' of
        # sale order line was not set.
        self.assertEqual(sale_order.order_line, shipment_plan.origin_sale_line_ids)
        # It works correctly, if we do this in Web Client.
        # So I have to set it here manually
        sale_order.order_line.trans_shipment_plan_id = shipment_plan
        # Create Transport Cost in Sale Order Line
        sale_order.action_create_trans_cost()
        # 1 lines for transport cost, 1 line for product_sale
        self.assertEqual(len(sale_order.order_line), 2)
        check_prod_cost = False
        for line in sale_order.order_line:
            if line.product_id.id == self.product_cost.id:
                self.assertEqual(line.price_unit, 630)
                check_prod_cost = True
        self.assertTrue(check_prod_cost)
        # Cancel the Sale Order
        sale_order.action_cancel()
        self.assertTrue(all(o.state == "cancel" for o in sale_order.trans_po_ids))
        self.assertTrue(all(o.state == "cancel" for o in sale_order.trans_pr_ids))
        self.assertTrue(
            all(o.state == "cancel" for o in sale_order.trans_shipment_plan_ids)
        )

    def test_02_shipment_plan_sale_singel_po(self):
        """
        2. Create SO for product_sale
        3. Run wizard create.sale.trans.request:
            To Create singel PO, Shipment Plan
        """
        sale_order = self._create_sale_order()
        self.assertTrue(sale_order.trans_pr_needed)
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
                }
            )
            .create(
                {
                    "multi": False,
                    "partner_id": self.partnerA.id,
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
        shipment_plan = wizard.action_confirm()
        wizard = (
            self.env["create.sale.trans.request"]
            .with_context(
                {
                    "active_id": sale_order.id,
                }
            )
            .create(
                {
                    "multi": False,
                    "partner_id": self.partnerA.id,
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
        shipment_plan = wizard.action_confirm()
        self.assertEqual(shipment_plan.trans_po_count, 1)
        self.assertEqual(shipment_plan.trans_pr_count, 1)
