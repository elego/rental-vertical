# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_vehicle_number = fields.Boolean("Show Vehicle Identification Number")
    show_license_plate = fields.Boolean("Show License Plate")
    show_init_regist = fields.Boolean('Show Initial Registration')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    further_ref = fields.Char("Further Reference")
    qr_code = fields.Char('QR-Code')
    manu_year = fields.Char('Year of Manufacture')
    manu_id = fields.Many2one('product.manufacturer', 'Manufacturer') #Marke
    manu_type_id = fields.Many2one('product.manufacturer.type', 'Type', ondelete='set null') #Marke Typ
    fleet_type_id = fields.Many2one('fleet.type', 'Fleet Type', ondelete='set null') #Flottentyp

    #Category special fields
    vehicle_number = fields.Char("Vehicle Identification Number")
    license_plate = fields.Char("License Plate")
    init_regist = fields.Date('Initial Registration')
    show_vehicle_number = fields.Boolean("Show Vehicle Identification Number", related="categ_id.show_vehicle_number")
    show_license_plate = fields.Boolean("Show License Plate", related="categ_id.show_license_plate")
    show_init_regist = fields.Boolean('Show Initial Registration', related="categ_id.show_init_regist")

    #sol_ids = fields.One2many('sale.order.line', 'product_id', string='Sale Order Lines')
    #inv_line_ids = fields.One2many('account.invoice.line', 'product_id', string='Invoice Lines')
    #po_line_ids = fields.One2many('purchase.order.line', 'product_id', string='Purchase Order Lines')
    rental_order_ids = fields.One2many('sale.rental', 'rented_product_id', string='Rental Orders')
    stock_move_ids = fields.One2many('stock.move', 'product_id', string='Stock Moves')
    additional_info = fields.Html('Additional Infomation')
    dimension = fields.Char('Dimension')

    invoice_count = fields.Integer(compute="_compute_invoice_count",
        string='Invoices', help='Total number of Invoice Orders')
    so_count = fields.Integer(compute="_compute_so_count",
        string='Sales', help='Total number of Sale Orders')
    po_count = fields.Integer(compute="_compute_po_count",
        string='Purchase', help='Total number of Purchase Orders')
    rental_count = fields.Integer(compute="_compute_rental_count",
        string='Rental', help='Total number of Rental Orders')

    @api.multi
    def _get_sale_order_ids(self, type_id):
        self.ensure_one()
        sols = self.env['sale.order.line'].search([
            ('product_id','=',self.id)])
        return list(set([l.order_id.id for l in sols if l.order_id.type_id == type_id]))

    @api.multi
    def action_view_sale_order(self):
        self.ensure_one()
        type_id = self.env.ref('sale_order_type.normal_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        for rental_service in self.rental_service_ids:
            record_ids += rental_service._get_sale_order_ids(type_id)
        record_ids = list(set(record_ids))
        action = self.env.ref('sale.action_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_rental_order(self):
        self.ensure_one()
        type_id = self.env.ref('rental_base.rental_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        for rental_service in self.rental_service_ids: 
            record_ids += rental_service._get_sale_order_ids(type_id)
        record_ids = list(set(record_ids))
        action = self.env.ref('rental_base.action_rental_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_all_purchase_order(self):
        self.ensure_one()
        pols = self._get_related_records(model='purchase.order.line')
        record_ids = list(set([l.order_id.id for l in pols]))
        tree_view_id = self.env.ref("purchase.purchase_order_tree").id
        form_view_id = self.env.ref("purchase.purchase_order_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Purchase Orders'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'purchase.order',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            'context': "{'search_default_group_by_order_type': 1}"
            }

    @api.multi
    def action_view_all_invoice(self):
        self.ensure_one()
        invls = self._get_related_records(model='account.invoice.line')
        record_ids = list(set([l.invoice_id.id for l in invls]))
        tree_view_id = self.env.ref("account.invoice_tree").id
        form_view_id = self.env.ref("purchase.invoice_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Invoices'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'account.invoice',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            'context': "{'search_default_group_by_type': 1}"
            }

    @api.multi
    def _get_related_records(self, model):
        self.ensure_one()
        records = self.env[model].search(
            [('product_id', '=', self.id)])
        return records

    @api.multi
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec._get_related_records(
                model='account.invoice.line'))

    @api.multi
    def _compute_so_count(self):
        type_id = self.env.ref('sale_order_type.normal_sale_type')
        for rec in self:
            rec.so_count = len(rec._get_sale_order_ids(type_id))

    @api.multi
    def _compute_rental_count(self):
        type_id = self.env.ref('rental_base.rental_sale_type')
        for rec in self:
            rec.rental_count = len(rec._get_sale_order_ids(type_id))

    @api.multi
    def _compute_po_count(self):
        for rec in self:
            rec.po_count = len(rec._get_related_records(
                model='purchase.order.line'))


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _description = 'Product Manufacturer'

    name = fields.Char('Name')
    manufacturer_type_ids = fields.One2many('product.manufacturer.type', 'manufacturer_id')


class ProductManufacturerType(models.Model):
    _name = 'product.manufacturer.type'
    _description = 'Product Manufacturer Type'

    name = fields.Char('Name')
    manufacturer_id = fields.Many2one('product.manufacturer', 'Manufacturer')


class FleetType(models.Model):
    _name = 'fleet.type'
    _description = 'Fleet Type'

    name = fields.Char('Name')
