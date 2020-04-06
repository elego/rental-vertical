from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError

from datetime import date, timedelta

import logging
_logger = logging.getLogger(__name__)


#@tagged('post_install', '-at_install')
#class TestRentalInvoice(AccountingTestCase):

    #def setUp(self):
        #super(TestRentalInvoice, self).setUp()

        #self.wizard_obj = self.env['account.invoice.create_forward_invoice']

        #self.date_start = date.today()
        #self.date_end = self.date_start + timedelta(days=28)

        #self.account_expense = self.env['account.account'].search(
            #[('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)],
            #limit=1
        #)
        #self.account_receivable = self.env['account.account'].search(
            #[('user_type_id', '=', self.env.ref('account.data_account_type_receivable').id)],
            #limit=1
        #)

        #self.analytic_account = self.env['account.analytic.account'].create({
            #'name': 'Office',
            #'code': '99999',
        #})

        #self.product = self.env['product.product'].create({
            #'name': 'Telephone Fees',
            #'default_code': '09233',
            #'type': 'service',
            #'sale_ok': False,
            #'purchase_ok': True,
            #'standard_price': 24.99,
        #})

        #self.vendor_bill = self.env['account.invoice'].create({
            #'partner_id': self.env.ref('base.res_partner_1').id,
            #'type': 'in_invoice',
            #'account_id': self.account_receivable.id,
            #'invoice_line_ids': [(0, 0, {
                #'product_id': self.product.id,
                #'name': self.product.display_name,
                #'quantity': 1.0,
                #'product_uom': self.product.uom_id.id,
                #'price_unit': self.product.standard_price,
                #'start_date': self.date_start,
                #'end_date': self.date_end,
                #'account_id': self.account_expense.id,
                #'account_analytic_id': self.analytic_account.id,
            #})],
        #})

    #def test_01_invoice_factual_check(self):
        #self.assertFalse(self.vendor_bill.factually_correct)

        #self.vendor_bill.action_set_factual_check_failed()
        #self.assertEqual(self.vendor_bill.factually_correct, 'no')

        #self.vendor_bill.action_set_factual_check_succeeded()
        #self.assertEqual(self.vendor_bill.factually_correct, 'yes')

    #def test_02_invoice_arithmetical_check(self):
        #self.assertFalse(self.vendor_bill.arithmetically_correct)

        #self.vendor_bill.action_set_arithmetical_check_failed()
        #self.assertEqual(self.vendor_bill.arithmetically_correct, 'no')

        #self.vendor_bill.action_set_arithmetical_check_succeeded()
        #self.assertEqual(self.vendor_bill.arithmetically_correct, 'yes')

    #def test_03_invoice_create_outgoing_invoice(self):
        #self.assertFalse(self.vendor_bill.customer_invoice_needed)
        #self.assertEqual(self.vendor_bill.customer_invoice_count, 0)
        #self.assertFalse(self.vendor_bill.has_non_canceled_customer_invoices)

        #self.vendor_bill.write({'customer_invoice_needed': True})
        #self.assertTrue(self.vendor_bill.customer_invoice_needed)
        #self.assertEqual(self.vendor_bill.customer_invoice_count, 0)
        #self.assertFalse(self.vendor_bill.has_non_canceled_customer_invoices)

        #wizard = self.wizard_obj.with_context(active_ids=[self.vendor_bill.id]).create({
            #'partner_id': self.env.ref('base.res_partner_2').id
        #})

        ## product in invoice line is not sellable
        #with self.assertRaises(ValidationError) as e:
            #wizard.create_forward_invoice()
        #self.assertIn(
            #'The customer invoice cannot be created because the following products are not sellable:',
            #e.exception.name)
        #self.assertEqual(self.vendor_bill.customer_invoice_count, 0)
        #self.assertFalse(self.vendor_bill.has_non_canceled_customer_invoices)

        #self.product.write({'sale_ok': True})
        #wizard.create_forward_invoice()
        #self.vendor_bill._compute_customer_invoices()

        #self.assertEqual(self.vendor_bill.customer_invoice_count, 1)
        #self.assertTrue(self.vendor_bill.has_non_canceled_customer_invoices)

        #invoice = self.vendor_bill.customer_invoice_ids[0]
        #invoice_line = invoice.invoice_line_ids[0]
        #vendor_bill_line = self.vendor_bill.invoice_line_ids[0]

        #self.assertEqual(invoice.type, 'out_invoice')
        #self.assertEqual(invoice_line.product_id.id, vendor_bill_line.product_id.id)
        #self.assertEqual(invoice_line.quantity, vendor_bill_line.quantity)
        #self.assertEqual(invoice_line.price_unit, vendor_bill_line.price_unit)
        #self.assertEqual(invoice_line.discount, vendor_bill_line.discount)
        #self.assertEqual(invoice_line.start_date, vendor_bill_line.start_date)
        #self.assertEqual(invoice_line.end_date, vendor_bill_line.end_date)
        #self.assertEqual(invoice_line.end_date, vendor_bill_line.end_date)
        #self.assertEqual(invoice_line.account_analytic_id.id, vendor_bill_line.account_analytic_id.id)

        #invoice.action_cancel()
        #self.vendor_bill._compute_customer_invoices()
        #self.assertEqual(self.vendor_bill.customer_invoice_count, 1)
        #self.assertFalse(self.vendor_bill.has_non_canceled_customer_invoices)
