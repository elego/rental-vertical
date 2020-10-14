# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import os
import base64
from odoo import fields, exceptions
from odoo.tests.common import TransactionCase
from datetime import date, datetime as dt, timedelta

import logging
_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)


class TestRentalTollCollect(TransactionCase):
    """ Test Rental Toll Collect"""

    def setUp(self):
        super(TestRentalTollCollect, self).setUp()

        SaleOrderObj = self.env['sale.order']
        ProductObj = self.env['product.product']
        TollLineObj = self.env['toll.charge.line']

        self.now = dt.now()
        self.date_10_day_before = self.now - timedelta(days=10)
        self.date_15_day_before = self.now - timedelta(days=15)
        self.date_20_day_before = self.now - timedelta(days=20)
        self.today = date.today()
        self.start_date = self.today - timedelta(days=30)
        self.end_date = self.today
        self.uom_month = self.env.ref('rental_base.product_uom_month')
        self.uom_day = self.env.ref('uom.product_uom_day')
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        self.rental_sale_type = self.env.ref('rental_base.rental_sale_type')
        self.partner = self.env.ref('base.res_partner_1')
        self.pricelist = self.env.ref('product.list0')
        self.toll_product = self.env.ref('rental_toll_collect.product_toll')

        # Create Product Test Import
        self.import_product = ProductObj.create({
            'name': 'Test Import',
            'type': 'product',
            'rental': True,
            'rental_of_month': True,
            'rental_of_day': True,
            'rental_of_hour': False,
            'rental_price_month': 4500,
            'rental_price_day': 200,
            'license_plate': 'BNA 1830',
        })
        self.assertEqual(len(self.import_product.rental_service_ids), 2)

        # Create Product A
        self.product = ProductObj.create({
            'name': 'Product A',
            'type': 'product',
            'rental': True,
            'rental_of_month': True,
            'rental_of_day': True,
            'rental_of_hour': False,
            'rental_price_month': 4500,
            'rental_price_day': 200,
            'license_plate': 'BNA 1831',
        })
        self.assertEqual(len(self.product.rental_service_ids), 2)
        self.day_service_product = self.product.product_rental_day_id

        # create toll charge lines for Product A
        self.line_01 = TollLineObj.create({
            'license_plate': 'BNA 1831',
            'axle_class': '2',
            'weight_class': '4',
            'polution_class': '7',
            'toll_type': 'toll',
            'procedure': 'AV',
            'start_date': self.date_10_day_before,
            'start_time': '11:00',
            'booking_number': '100000000000101',
            'chargeable': True,
            'distance': 6.2,
            'amount': 1.25,
        })
        self.line_02 = TollLineObj.create({
            'license_plate': 'BNA 1831',
            'axle_class': '2',
            'weight_class': '4',
            'polution_class': '7',
            'toll_type': 'toll',
            'procedure': 'AV',
            'start_date': self.date_15_day_before,
            'start_time': '11:00',
            'booking_number': '100000000000102',
            'chargeable': True,
            'distance': 7.2,
            'amount': 1.50,
        })
        self.line_03 = TollLineObj.create({
            'license_plate': 'BNA 1831',
            'axle_class': '2',
            'weight_class': '4',
            'polution_class': '7',
            'toll_type': 'toll',
            'procedure': 'AV',
            'start_date': self.date_20_day_before,
            'start_time': '11:00',
            'booking_number': '100000000000103',
            'chargeable': True,
            'distance': 8.2,
            'amount': 1.75,
        })
        val = {
            'display_product_id': self.product.id,
            'product_id': self.day_service_product.id,
            'name': self.day_service_product.name,
            'rental': True,
            'rental_type': 'new_rental',
            'rental_qty': 1.0,
            'product_uom': self.day_service_product.uom_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        self.sale_order = SaleOrderObj.create({
            'partner_id': self.partner.id,
            'type_id': self.rental_sale_type.id,
            'pricelist_id': self.pricelist.id,
            'default_start_date': self.start_date,
            'default_end_date': self.end_date,
            'order_line': [(0, 0, val)],
        })
        self.assertEqual(len(self.sale_order.order_line), 1)
        self.so_line = self.sale_order.order_line[0]

    def run_import_toll_charge_lines(self, file_name, file_type):
        with open(os.path.join(_path, 'tests/data', file_name), 'rb') as file:
            import_wizard = self.env['toll.charge.line.import'].create({
                'data_file': base64.b64encode(file.read()),
                'filename': file_name})
            import_wizard.import_toll_charge_lines()
            domain = [('booking_number', 'in', ['100000000000051', '100000000000052', '100000000000053'])]
            lines = self.env['toll.charge.line'].search(domain)
            self.assertEqual(len(lines), 3)
            self.assertEqual(lines.mapped('product_id'), self.import_product)
            self.assertEqual(lines.mapped('amount'),[6.91, 2.93, 0.27])
            self.assertEqual(lines.mapped('distance'),[39.9, 16.9, 1.6])
            self.assertEqual(lines.mapped('chargeable'),[True, True, True])

    def test_01_toll_charge_lines(self):
        """
            check toll charge lines values
        """
        start = dt.strptime('11:00', "%H:%M")
        offset = start - dt.strptime("00:00", "%H:%M")
        # checks for line_01
        toll_date = self.date_10_day_before + offset
        self.assertEqual(self.line_01.product_id, self.product)
        self.assertEqual(self.line_01.toll_date, toll_date)
        # checks for line_02
        toll_date = self.date_15_day_before + offset
        self.assertEqual(self.line_02.product_id, self.product)
        self.assertEqual(self.line_02.toll_date, toll_date)
        # checks for line_03
        toll_date = self.date_20_day_before + offset
        self.assertEqual(self.line_03.product_id, self.product)
        self.assertEqual(self.line_03.toll_date, toll_date)

    def test_02_rental_so_toll_charge_line(self):
        """
            check toll charge lines after creating sale order
        """
        self.so_line.onchange_rental()
        self.so_line.rental_product_id_change()
        self.so_line.product_uom_change()
        self.so_line.product_id_change()
        self.so_line.onchange_start_end_date()
        self.so_line.rental_qty_number_of_days_change()
        # checks rental values
        self.assertEqual(len(self.sale_order.order_line), 1)
        self.assertEquals(self.so_line.product_uom, self.uom_day)
        self.assertEquals(self.so_line.rental_type, 'new_rental')
        self.assertEquals(self.so_line.rental, True)
        self.assertEquals(self.so_line.start_date, self.start_date)
        self.assertEquals(self.so_line.end_date, self.end_date)
        self.assertEquals(self.so_line.product_uom_qty, 31.0)
        self.assertEquals(self.so_line.rental_qty, 1.0)
        self.sale_order.action_update_toll_charges()
        self.so_line.update_toll_charge_lines()
        self.so_line.onchange_toll_lines_params()
        # checks toll charge line count after update
        self.assertEquals(self.sale_order.toll_line_count, 3)
        self.assertEquals(self.sale_order.toll_line_charged_count, 0)
        self.assertEquals(self.sale_order.update_toll_lines, True)

    def test_03_rental_so_to_invoice_toll_charge_lines(self):
        self.sale_order.action_confirm()
        # create an invoice with invoiceable lines
        wiz_inv = self.env['sale.advance.payment.inv'].with_context(
            active_ids=[self.sale_order.id]).create({
            'advance_payment_method': 'delivered',
        })
        wiz_inv.create_invoices()
        self.assertEqual(len(self.sale_order.invoice_ids), 1)
        self.invoice = self.sale_order.invoice_ids[0]
        self.invoice.action_invoice_open()
        self.invoice.action_update_toll_charges()
        # checks toll charge line count,invoice lines after update
        self.assertEquals(self.invoice.toll_line_count, 3)
        self.assertEquals(self.invoice.toll_line_charged_count, 3)
        self.assertEqual(self.invoice.sale_type_id, self.rental_sale_type,
            "Sale Type of Invoice must be Rental Order")
        for line in self.invoice.invoice_line_ids:
            line.update_toll_charge_lines()
            line.onchange_toll_lines_params()
            self.assertEquals(
                line.account_analytic_id,
                line.product_id.income_analytic_account_id)
        self.assertEqual(len(self.invoice.invoice_line_ids), 2)
        self.assertEquals(self.invoice.invoice_line_ids[0].product_id, self.day_service_product)
        self.assertEquals(self.invoice.invoice_line_ids[0].uom_id, self.uom_day)
        self.assertEquals(self.invoice.invoice_line_ids[1].product_id, self.toll_product)
        self.assertEquals(self.invoice.invoice_line_ids[1].uom_id, self.uom_unit)
        self.assertEquals(self.invoice.invoice_line_ids.mapped('name'), [
        'Rental of Product A (Day(s))',
        'Toll Charges for BNA 1831 Total Distance: 21.6 km'])
        self.assertEquals(self.invoice.invoice_line_ids.mapped('price_unit'), [200.00, 4.50])
        self.assertEquals(self.invoice.update_toll_lines, True)
        # update toll charge line
        self.line_01.write({'chargeable': False, 'invoiced': False})
        for inv_line in self.invoice.invoice_line_ids:
            inv_line.update_toll_charge_lines()
        self.invoice.action_update_toll_charges()
        self.invoice._compute_toll_charged_count()
        self.assertEquals(self.invoice.toll_line_count, 3)
        self.assertEquals(self.invoice.toll_line_charged_count, 2)
        self.assertEquals(self.invoice.invoice_line_ids.mapped('name'), [
        'Rental of Product A (Day(s))',
        'Toll Charges for BNA 1831 Total Distance: 15.4 km'])
        self.assertEquals(self.invoice.invoice_line_ids.mapped('price_unit'), [200.00, 3.25])
        self.assertEquals(self.sale_order.toll_line_count, 3)
        self.assertEquals(self.sale_order.toll_line_charged_count, 2)

    def test_04_import_csv_toll_charge_lines(self):
        self.run_import_toll_charge_lines(
            'test_toll_charge_line.csv',
            'text/csv')
