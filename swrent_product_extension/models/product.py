# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_instance = fields.Boolean(string='Product Instance', default=False,
        help='This product is a product instance, which can only have one unit in stock.')

    @api.onchange('product_instance')
    def onchange_product_instance(self):
        if self.product_instance:
            self.tracking = 'serial'

    @api.onchange('tracking')
    def onchange_tracking(self):
        res = super(ProductTemplate, self).onchange_tracking()
        if self.tracking != 'serial':
            self.product_instance = False
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    qr_code = fields.Char('QR-Code')
    manu_year = fields.Char('Year of Manufacture')

    instance_serial_number_id = fields.Many2one('stock.production.lot', 'Serial Number', ondelete='set null', domain="[('product_id', '=', id)]")

    brand = fields.Many2one('product.brand', ' Brand') #Marke
    brand_type = fields.Many2one('product.brand.type', 'Branch Type', ondelete='set null') #Marke Typ
    fleet_type = fields.Many2one('fleet.type', 'Fleet Type', ondelete='set null') #Flottentyp

    #sol_ids = fields.One2many('sale.order.line', 'product_id', string='Sale Order Lines')
    #inv_line_ids = fields.One2many('account.invoice.line', 'product_id', string='Invoice Lines')
    #po_line_ids = fields.One2many('purchase.order.line', 'product_id', string='Purchase Order Lines')
    rental_order_ids = fields.One2many('sale.rental', 'rented_product_id', string='Rental Orders')
    repair_order_ids = fields.One2many('repair.order', 'product_id', string='Repair Orders')
    stock_move_ids = fields.One2many('stock.move', 'product_id', string='Stock Moves')

    product_timeline_ids = fields.One2many('product.timeline', 'product_id', 'Time Lines')

    @api.onchange('product_instance')
    def onchange_product_instance(self):
        if self.product_instance:
            self.tracking = 'serial'

    @api.onchange('tracking')
    def onchange_tracking(self):
        res = super(ProductProduct, self).onchange_tracking()
        if self.tracking != 'serial':
            self.product_instance = False
        return res

    @api.multi
    def _get_all_sale_order_ids(self):
        self.ensure_one()
        sols = self.env['sale.order.line'].search([('product_id','=',self.id)])
        return list(set([l.order_id.id for l in sols]))

    @api.multi
    def action_view_all_sale_order(self):
        self.ensure_one()
        record_ids = self._get_all_sale_order_ids()
        for rental_service in self.rental_service_ids: 
            record_ids += rental_service._get_all_sale_order_ids()
        record_ids = list(set(record_ids))
        view_id = self.env.ref("sale.view_order_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Sale Orders'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'sale.order',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    @api.multi
    def action_view_all_purchase_order(self):
        self.ensure_one()
        pols = self.env['purchase.order.line'].search([('product_id', '=', self.id)])
        record_ids = list(set([l.order_id.id for l in pols]))
        view_id = self.env.ref("purchase.purchase_order_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Purchase Orders'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'purchase.order',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    @api.multi
    def action_view_all_invoice(self):
        self.ensure_one()
        invls = self.env['account.invoice.line'].search([('product_id', '=', self.id)])
        record_ids = list(set([l.invoice_id.id for l in invls]))
        view_id = self.env.ref("account.invoice_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Invoices'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'account.invoice',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char('Name')
    brand_type_ids = fields.One2many('product.brand.type', 'brand_id')


class ProductBrandType(models.Model):
    _name = 'product.brand.type'
    _description = 'Product Brand Type'

    name = fields.Char('Name')
    brand_id = fields.Many2one('product.brand', 'Brand')


class FleetType(models.Model):
    _name = 'fleet.type'
    _description = 'Fleet Type'

    name = fields.Char('Name')
