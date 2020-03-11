# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class RentalStockCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()

        # Picking Type and Locations
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.picking_type_out = self.env.ref('stock.picking_type_out')
        self.stock_location = self.env.ref('stock.stock_location_stock')
        self.supplier_location = self.env.ref('stock.stock_location_suppliers')
        self.customer_location = self.env.ref('stock.stock_location_customers')
        self.uom_day = self.env.ref('uom.product_uom_day')
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        self.uom_kgm = self.env.ref('uom.product_uom_kgm')

        self.PartnerObj = self.env['res.partner']
        self.partnerA = self.PartnerObj.create({
            'name': 'Partner A',
            'customer': True,
            'supplier': True,
            'country_id': self.env.ref('base.de').id,
        })

    def _create_rental_service_day(self, product):
        values = {
            'hw_product_id': product.id,
            'name': 'Rental of %s (Day)' % product.name,
            'categ_id': product.categ_id.id,
            'copy_image': True,
        }
        res = self.env['create.rental.product'].with_context(
            active_model='product.product',
            active_id=product.id).create(values).create_rental_product()

        rental_service = self.env['product.product'].browse(res['res_id'])
        rental_service.write({
            'uom_id': self.uom_day.id,
            'uom_po_id': self.uom_day.id,
            'list_price': 100})

        return rental_service

    def _print_move(self, move):
        print('-------------%s--------------' % move)
        print(move.product_id.name)
        print(move.product_uom_qty)
        print(move.location_id.name)
        print(move.location_dest_id.name)
