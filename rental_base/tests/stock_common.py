# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class RentalStockCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()

        # Rental Type, Picking Type, Locations and Uoms
        self.rental_sale_type = self.env.ref('rental_base.rental_sale_type')
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.picking_type_out = self.env.ref('stock.picking_type_out')
        self.stock_location = self.env.ref('stock.stock_location_stock')
        self.supplier_location = self.env.ref('stock.stock_location_suppliers')
        self.customer_location = self.env.ref('stock.stock_location_customers')
        self.uom_hour = self.env.ref('uom.product_uom_hour')
        self.uom_day = self.env.ref('uom.product_uom_day')
        self.uom_month = self.env.ref('rental_base.product_uom_month')
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

    def _create_move(self, product, src_location, dst_location, **values):
        Move = self.env['stock.move']
        move = Move.new({
            'product_id': product.id,
            'location_id': src_location.id,
            'location_dest_id': dst_location.id
        })
        move.onchange_product_id()
        move_values = move._convert_to_write(move._cache)
        move_values.update(**values)
        return Move.create(move_values)

    def _print_move(self, move):
        print('-------------%s--------------' % move)
        print(move.state)
        if move.picking_id:
            print("picking: %s" % move.picking_id.state)
        print(move.product_id.name)
        print(move.product_uom_qty)
        print(move.product_uom.name)
        print(move.location_id.name)
        print(move.location_dest_id.name)
        print(move.move_line_ids.lot_id)
