# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields
from odoo.exceptions import ValidationError

class TestRentalContractInsurance(RentalStockCommon):

    def setUp(self):
        super().setUp()

        self.analytic_account = self.env['account.analytic.account'].create({
            'name': 'Analytic Account A',
            'code': '100000',
        })

        # Product Created A
        ProductObj = self.env['product.product']
        self.productA = ProductObj.create({
            'name': 'Product A',
            'type': 'product',
            'standard_price': 10000,
        })
        self.productA.write({
            'rental': True,
            'rental_of_month': True,
            'rental_of_day': True,
            'rental_price_month': 1000,
            'rental_price_day': 100,
            'income_analytic_account_id': self.analytic_account.id,
        })
        self.contract_template = self.env.ref(
            'rental_contract.rental_contract_template')
        # P - Productcost, R - Rentalcost, D - Day, M - Month
        self.insurancePD = ProductObj.create({
            'name': 'Insurance P D',
            'type': 'service',
            'is_insurance': True,
            'uom_id': self.uom_day.id,
            'uom_po_id': self.uom_day.id,
        })
        self.insurancePM = ProductObj.create({
            'name': 'Insurance P M',
            'type': 'service',
            'is_insurance': True,
            'is_contract': True,
            'property_contract_template_id': self.contract_template.id,
            'uom_id': self.uom_month.id,
            'uom_po_id': self.uom_month.id,
        })
        self.insuranceRD = ProductObj.create({
            'name': 'Insurance R D',
            'type': 'service',
            'is_insurance': True,
            'uom_id': self.uom_day.id,
            'uom_po_id': self.uom_day.id,
        })
        self.insuranceRM = ProductObj.create({
            'name': 'Insurance R M',
            'type': 'service',
            'is_insurance': True,
            'is_contract': True,
            'property_contract_template_id': self.contract_template.id,
            'uom_id': self.uom_month.id,
            'uom_po_id': self.uom_month.id,
        })

        self.productA.write({
            'day_insurance_product_ids': [
                (0, 0, {
                    'product_id': self.productA.id,
                    'insurance_product_id': self.insurancePD.id,
                    'insurance_type': 'product',
                    'insurance_percent': 2,
                }),
                (0, 0, {
                    'product_id': self.productA.id,
                    'insurance_product_id': self.insuranceRD.id,
                    'insurance_type': 'rental',
                    'insurance_percent': 10,
                })
            ],
            'month_insurance_product_ids': [
                (0, 0, {
                    'product_id': self.productA.id,
                    'insurance_product_id': self.insurancePM.id,
                    'insurance_type': 'product',
                    'insurance_percent': 20,
                }),
                (0, 0, {
                    'product_id': self.productA.id,
                    'insurance_product_id': self.insuranceRM.id,
                    'insurance_type': 'rental',
                    'insurance_percent': 10,
                })
            ],
        })

        self.today = fields.Date.from_string(fields.Date.today())
        self.date_three_month_later = self.today + relativedelta(months=3)
        self.date_19_later = self.today + relativedelta(days=19)
        self.rental_order = self.env['sale.order'].with_context({
            'default_type_id': self.rental_sale_type.id,
        }).create({
            'partner_id': self.partnerA.id,
            'pricelist_id': self.env.ref('product.list0').id,
        })

    def _run_sol_onchange_display_product_id(self, line):
        line.onchange_display_product_id() # product_id, rental changed
        line.product_id_change()
        line.onchange_rental() # product_id changed again
        line.product_id_change() # product_uom changed
        line.product_uom_change()
        line.rental_product_id_change() # set start end date manually

    def _run_sol_onchange_product_uom(self, line, product_uom):
        line.product_uom = product_uom
        line.product_uom_change()
        line.product_id_change()
        line.onchange_start_end_date()
        line.start_date_change()
        line.end_date_change()
        line.rental_qty_number_of_days_change()
        line.product_uom_change()

    def test_00_rental_insurance_day_and_month(self):
        # create sale order line
        line = self.env['sale.order.line'].with_context({
            'type_id': self.rental_sale_type.id,
        }).new({
            'display_product_id': self.productA.id,
            'start_date': self.today,
            'end_date': self.date_19_later,
        })
        self._run_sol_onchange_display_product_id(line)
        self._run_sol_onchange_product_uom(line, self.uom_day)
        line.onchange_insurance_product_id()
        vals = line._convert_to_write(line._cache)
        vals['order_id'] = self.rental_order.id
        order_line = self.env['sale.order.line'].create(vals)
        self.assertEqual(len(self.rental_order.order_line), 3)
        self.assertEqual(len(order_line.insurance_product_ids), 2)

        # check sale order line for insurancePD and insuranceRD
        check_insurancePD = False
        check_insuranceRD = False
        for line in self.rental_order.order_line:
            if line.product_id == self.insurancePD:
                self.assertEqual(line.price_unit, 200)
                self.assertEqual(line.product_uom_qty, 20)
                self.assertEqual(
                    line.insurance_origin_line_id.id,
                    order_line.id
                )
                self.assertEqual(line.name, self.insurancePD.name)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insurancePD = True
            if line.product_id == self.insuranceRD:
                self.assertEqual(line.price_unit, 10)
                self.assertEqual(line.product_uom_qty, 20)
                self.assertEqual(
                    line.insurance_origin_line_id.id,
                    order_line.id
                )
                self.assertEqual(line.name, self.insuranceRD.name)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insuranceRD = True
        self.assertEqual(check_insurancePD, True)
        self.assertEqual(check_insuranceRD, True)

        # change product_uom to Month
        order_line.write({
            'start_date': self.today,
            'end_date': self.date_three_month_later,
        })
        with self.assertRaises(ValidationError):
            order_line.product_uom = self.uom_month
        order_line.insurance_product_ids.unlink()
        self._run_sol_onchange_product_uom(order_line, self.uom_month)
        order_line.onchange_insurance_product_id()
        self.assertEqual(len(order_line.insurance_product_ids), 2)
        order_line.onchange_insurance_params()
        order_line.update_rental_insurance_line()

        # check sale order line for insurancePM and insuranceRM
        check_insurancePM = False
        check_insuranceRM = False
        for line in self.rental_order.order_line:
            if line.product_id == self.insurancePM:
                self.assertEqual(line.price_unit, 2000)
                self.assertEqual(line.product_uom_qty, 3)
                self.assertEqual(line.name, self.insurancePM.name)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insurancePM = True
            if line.product_id == self.insuranceRM:
                self.assertEqual(line.price_unit, 100)
                self.assertEqual(line.product_uom_qty, 3)
                self.assertEqual(line.name, self.insuranceRM.name)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insuranceRM = True
        self.assertEqual(check_insurancePM, True)
        self.assertEqual(check_insuranceRM, True)

    def test_01_rental_contract_insurance(self):
        line = self.env['sale.order.line'].with_context({
            'type_id': self.rental_sale_type.id,
        }).new({
            'display_product_id': self.productA.id,
            'start_date': self.today,
            'end_date': self.date_three_month_later,
        })
        self._run_sol_onchange_display_product_id(line)
        line.insurance_product_ids.unlink()
        self._run_sol_onchange_product_uom(line, self.uom_month)
        line.onchange_insurance_product_id()
        line.onchange_insurance_params()
        self.assertEqual(len(line.insurance_product_ids), 2)
        vals = line._convert_to_write(line._cache)
        vals['order_id'] = self.rental_order.id
        line  = self.env['sale.order.line'].create(vals)
        self.rental_order.action_confirm()
        self.assertEqual(self.rental_order.contract_count, 1)
        check_insurance_line = False
        for line in self.rental_order.order_line:
            if line.product_id == self.insurancePM:
                self.assertEqual(line.date_start, self.today)
                self.assertEqual(line.date_end, self.date_three_month_later)
                contract_line = line.contract_id.contract_line_ids[0]
                self.assertEqual(contract_line.date_start, self.today)
                self.assertEqual(contract_line.date_end, self.date_three_month_later)
                self.assertEqual(contract_line.analytic_account_id, self.analytic_account)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insurance_linePM = True
            if line.product_id == self.insuranceRM:
                self.assertEqual(line.date_start, self.today)
                self.assertEqual(line.date_end, self.date_three_month_later)
                contract_line = line.contract_id.contract_line_ids[0]
                self.assertEqual(contract_line.date_start, self.today)
                self.assertEqual(contract_line.date_end, self.date_three_month_later)
                self.assertEqual(contract_line.analytic_account_id, self.analytic_account)
                invoice_line_vals = line._prepare_invoice_line(1)
                self.assertEqual(invoice_line_vals['account_analytic_id'], self.analytic_account.id)
                check_insurance_lineRM = True
        self.assertTrue(check_insurance_linePM, 'No found expected insurance line')
        self.assertTrue(check_insurance_lineRM, 'No found expected insurance line')


