# Part of rental-vertical See LICENSE file for full copyright and licensing details.
import odoo.tests


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):

    def test_01_rental_tour(self):
        self.phantom_js("/web", "odoo.__DEBUG__.services['web_tour.tour'].run('rental_tour')", "odoo.__DEBUG__.services['web_tour.tour'].tours.rental_tour.ready", login="admin")

#@tagged('post_install', '-at_install')
#class TestRentalSO(TestRentalPricelist):
#    """ Test renting of a product instance for 60 days including quotation and order"""
#    def setUp(self):
#        super(TestRentalSO, self).setUp()
#        self.today = date.today()
#        self.date_60_day_later = self.today + timedelta(days=60)
#        self.rental_sale_type = self.env.ref('rental_base.rental_sale_type')
#        self.product = self.env.ref('rental_product_instance.rental_01530')
#        self.product.rental_service_ids.write({
#            'income_analytic_account_id': self.product.income_analytic_account_id,
#            'expense_analytic_account_id': self.product.expense_analytic_account_id})
#        self.partner = self.env.ref('base.res_partner_12')
#        # add scale price of product
#        #    Day     Price
#        #      1     200
#        #     50      70
#        self.item = self.env['product.pricelist.item'].create({
#            'applied_on': '0_product_variant',
#            'compute_price': 'fixed',
#            'product_id': self.product.product_rental_day_id.id,
#            'pricelist_id': self.product.def_pricelist_id.id,
#            'min_quantity': 50,
#            'fixed_price': 70,
#        })
#        # sale order with type : Rental Order
#        self.rental_order = self.env['sale.order'].with_context({
#            'default_type_id': self.rental_sale_type.id,
#        }).create({
#            'partner_id': self.partner.id,
#            'pricelist_id': self.env.ref('product.list0').id,
#        })
#        line = self.env['sale.order.line'].with_context({
#            'type_id': self.rental_sale_type.id,
#        }).new({
#            'order_id': self.rental_order.id,
#            'display_product_id': self.product.id,
#            'start_date': self.today,
#            'end_date': self.date_60_day_later,
#        })
#        line.onchange_display_product_id()
#        res = line.product_id_change()
#        # Feature : check available uom coming from product
#        check_uom_domain = False
#        if 'domain' in res and 'product_uom' in res['domain']:
#            self.assertEqual(len(res['domain']['product_uom'][0][2]), 2)
#            check_uom_domain = True
#        self.assertTrue(check_uom_domain)
#        line.onchange_rental()
#        line.product_uom_change()
#        line.rental_product_id_change()
#        self._run_sol_onchange_date(line)
#        vals = line._convert_to_write(line._cache)
#        vals['order_id'] = self.rental_order.id
#        self.line = self.env['sale.order.line'].create(vals)
#
#    def test_02_check_price_scale(self):
#        self.item._onchange_product_id()
#        # Feature : check price scales on Product
#        self.assertEqual(self.item.day_item_id, self.product)
#        # Feature : check price scales while adding sol
#        self.assertEqual(self.line.product_uom_qty > 50, True)
#        self.assertEqual(self.line.price_unit, 70)
#        self._run_sol_onchange_date(self.line, end_date=self.date_60_day_later)
#        self._run_sol_onchange_date(self.line, end_date=self.tomorrow)
#        self.assertEqual(self.line.product_uom_qty, 2)
#        self.assertEqual(self.line.price_unit, 200)
#
#    def test_rental_so_to_invoice(self):
#        self.rental_order.action_confirm()
#        # create an invoice with invoiceable lines
#        wiz_inv = self.env['sale.advance.payment.inv'].with_context(
#            active_ids=[self.rental_order.id]).create({
#            'advance_payment_method': 'delivered',
#        })
#        wiz_inv.create_invoices()
#        self.invoice = self.rental_order.invoice_ids[0]
#        self.invoice.action_invoice_open()
#        # Feature : check Sale type on invoice
#        self.assertEqual(self.invoice.sale_type_id, self.rental_sale_type,
#            "Sale Type of Invoice must be same as on Sale Order")
#        # Feature : check analytic account on invoice line
#        for inv_line in self.invoice.invoice_line_ids:
#            self.assertEquals(
#                inv_line.account_analytic_id,
#                inv_line.product_id.income_analytic_account_id)
