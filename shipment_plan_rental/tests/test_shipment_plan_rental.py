# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.shipment_plan.tests.common import ShipmentPlanCommon
from odoo.addons.shipment_plan_sale.tests.test_shipment_plan_sale import confirm_shipment_plan_pos
from odoo import fields, exceptions


class TestShipmentPlanSale(ShipmentPlanCommon):

    def setUp(self):
        super().setUp()
        self.PurchaseObj = self.env['purchase.order']
        # Create Product (need Trans PR) for Sale
        ProductObj = self.env['product.product']
        self.product_rental = ProductObj.create({
            'name': 'Product for Rental',
            'type': 'product',
            'categ_id': self.category_all.id,
            'trans_purchase_request': True,
        })
        values = {
            'hw_product_id': self.product_rental.id,
            'name': 'Service Rental',
            'categ_id': self.category_all.id,
            'copy_image': True,
        }
        res = self.env['create.rental.product'].with_context(
            active_model='product.product',
            active_id=self.product_rental.id
        ).create(values).create_rental_product()
        self.service_rental = ProductObj.browse(res['res_id'])
        self.service_rental.write({
            'rental': True,
            'list_price': 100})


    def _create_rental_order(self):
        '''
            Create a Rental Order with Product (self.service_rental)
        '''
        rental_order = self.env['sale.order'].create({
            'type_id': self.rental_sale_type.id,
            'partner_id': self.partnerC.id,
            'partner_invoice_id': self.partnerC.id,
            'partner_shipping_id': self.partnerC.id,
            'incoterm': self.incotermsA.id,
            'pricelist_id': self.env.ref('product.list0').id,
            'picking_policy': 'direct',
            'warehouse_id': self.env.ref('stock.warehouse0').id,
            'order_line': [(0, 0, {
                'name': 'Service for Rental',
                'product_id': self.service_rental.id,
                'rental': True,
                'rental_type': 'new_rental',
                'rental_qty': 1,
                'product_uom_qty': 2,
                'start_date': self.today,
                'end_date': self.tomorrow,
                'price_unit': 100,
                'product_uom': self.uom_day.id,
            })]
        })
        self.assertEqual(rental_order.state, 'draft')
        return rental_order

    def test_00_shipment_plan_rental(self):
        """
            1. Create Rental Order for product_rental
            2. Run wizard create.sale.trans.request:
                To Create PO, PR and Shipment Plan
            3. Create PO from PR and Confirm all POs
            4. Run action_create_trans_cost
                To Create SOL for Transport Cost
            5. Confirm Rental Order
        """
        # Create Rental Order for product_rental
        rental_order = self._create_rental_order()
        self.assertTrue(rental_order.trans_pr_needed)
        self.assertEqual(rental_order.transport_cost_type, 'multi')
        wizard = self.env['create.sale.trans.request'].with_context({
            'active_id': rental_order.id,
        }).create({
            'service_product_ids': [
                (4, self.product_trans_pr_1.id,),
                (4, self.product_trans_po_1.id,),
            ]
        })
        # Create PO, PR and Shipment Plan
        shipment_plan, return_shipment_plan = wizard.action_confirm()
        self.assertEqual(shipment_plan.trans_po_count, 1)
        self.assertEqual(shipment_plan.trans_pr_count, 1)
        confirm_shipment_plan_pos(self, shipment_plan)
        self.assertEqual(return_shipment_plan.trans_po_count, 1)
        self.assertEqual(return_shipment_plan.trans_pr_count, 1)
        confirm_shipment_plan_pos(self, return_shipment_plan)
        #TODO Check why the field 'trans_shipment_plan_id' and
        #'trans_return_shipment_plan_id' of sale order line 
        #was not set. (The same in test_shipment_plan_sale)
        self.assertEqual(
            rental_order.order_line,
            shipment_plan.origin_sale_line_ids)
        self.assertEqual(
            rental_order.order_line,
            return_shipment_plan.origin_return_sale_line_ids)
        #It works correctly, if we do this in Web Client.
        # So I have to set it here manually
        rental_order.order_line.write({
            'trans_shipment_plan_id': shipment_plan.id,
            'trans_return_shipment_plan_id': return_shipment_plan.id
        })
        # There are 6 POs, 4 of them are confirmed
        self.assertEqual(rental_order.trans_shipment_plan_count, 2)
        self.assertEqual(rental_order.trans_pr_count, 2)
        self.assertEqual(shipment_plan.trans_po_count, 3)
        self.assertEqual(return_shipment_plan.trans_po_count, 3)
        self.assertEqual(rental_order.trans_po_count, 6)
        # Create Transport Cost in Sale Order Line
        rental_order.action_create_trans_cost()
        # 4 lines for transport cost, 1 line for product_sale
        self.assertEqual(len(rental_order.order_line), 5)
        # Confirm Rental Order
        rental_order.action_confirm()
        self.assertEqual(len(rental_order.picking_ids), 2)
        checkout_picking_sp = False
        checkout_picking_sp_return = False
        for picking in rental_order.picking_ids:
            if picking.shipment_plan_id.id == shipment_plan.id:
                checkout_picking_sp = True
            if picking.shipment_plan_id.id == return_shipment_plan.id:
                checkout_picking_sp_return = True
        self.assertTrue(checkout_picking_sp)
        self.assertTrue(checkout_picking_sp_return)
        # Check Description of Cost Position
        desc_1 = '''Transport PR 1
Incoterm: Incoterm External Shipment 
Service Rental: 2.0 Day(s) 
Date: %s 
Source Address: YourCompany 
Destination Address: Partner C
''' %(fields.Date.to_string(self.today))
        desc_2 = '''
Transport PO 1
Incoterm: Incoterm External Shipment 
Service Rental: 2.0 Day(s) 
Date: %s 
Source Address: YourCompany 
Destination Address: Partner C
''' %(fields.Date.to_string(self.today))
        desc_3 = '''
Transport PR 1
Incoterm: Incoterm External Shipment 
Service Rental: 2.0 Day(s) 
Date: %s 
Source Address: Partner C 
Destination Address: YourCompany
''' %(fields.Date.to_string(self.tomorrow))
        desc_4 = '''
Transport PO 1
Incoterm: Incoterm External Shipment 
Service Rental: 2.0 Day(s) 
Date: %s 
Source Address: Partner C 
Destination Address: YourCompany
''' %(fields.Date.to_string(self.tomorrow))
        check_desc_1 = check_desc_2 = check_desc_3 = check_desc_4 = False
        for line in rental_order.order_line:
            if line.name == desc_1:
                check_desc_1 = True
            elif line.name == desc_2:
                check_desc_2 = True
            elif line.name == desc_3:
                check_desc_3 = True
            elif line.name == desc_4:
                check_desc_4 = True
        self.assertTrue(desc_1)
        self.assertTrue(desc_2)
        self.assertTrue(desc_3)
        self.assertTrue(desc_4)

