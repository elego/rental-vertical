# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.tests import common
from odoo import fields, exceptions

class ShipmentPlanCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        # Create Transport Product
        ProductObj = self.env['product.product']
        SupplierObj = self.env['product.supplierinfo']
        PartnerObj = self.env['res.partner']
        self.incotermsA = self.env['account.incoterms'].create({
            'name': 'Incoterm External Shipment',
            'trans_pr_needed': True,
            'code': 'ext_shipment'
        })
        self.partnerA = PartnerObj.create({
            'name': 'Partner A',
            'customer': True,
            'supplier': True,
            'country_id': self.env.ref('base.de').id,
        })
        self.partnerB = PartnerObj.create({
            'name': 'Partner B',
            'customer': True,
            'supplier': True,
            'country_id': self.env.ref('base.de').id,
        })
        self.partnerC = PartnerObj.create({
            'name': 'Partner C',
            'customer': True,
            'country_id': self.env.ref('base.de').id,
        })
        self.product_cost = ProductObj.create({
            'name': 'Single Transport Cost',
            'type': 'service',
            'is_transport': True,
            'seller_ids': [
                (0, 0, {'name': self.partnerA.id, 'price': 10}),
            ]
        })
        self.product_trans_po_1 = ProductObj.create({
            'name': 'Transport PO 1',
            'type': 'service',
            'is_transport': True,
            'transport_service_type': 'po',
            'seller_ids': [
                (0, 0, {'name': self.partnerA.id, 'price': 100}),
            ]
        })
        self.product_trans_po_2 = ProductObj.create({
            'name': 'Transport PO 2',
            'type': 'service',
            'is_transport': True,
            'transport_service_type': 'po',
            'seller_ids': [
                (0, 0, {'name': self.partnerA.id, 'price': 200}),
            ]
        })
        self.product_trans_pr_1 = ProductObj.create({
            'name': 'Transport PR 1',
            'type': 'service',
            'is_transport': True,
            'transport_service_type': 'pr',
        })
        self.product_trans_pr_2 = ProductObj.create({
            'name': 'Transport PR 2',
            'type': 'service',
            'is_transport': True,
            'transport_service_type': 'pr',
        })

        self.today = fields.Date.from_string(fields.Date.today())
        self.date_one_month_later = self.today + relativedelta(months=1)
        self.from_address = PartnerObj.create({'name': 'From Address', 'type': 'delivery'})
        self.to_address = PartnerObj.create({'name': 'To Address', 'type': 'delivery'})


