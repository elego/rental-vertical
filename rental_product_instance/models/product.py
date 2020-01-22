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
            self.type = 'product'

    @api.onchange('tracking')
    def onchange_tracking(self):
        res = super(ProductTemplate, self).onchange_tracking()
        products = self.filtered(lambda self: self.tracking and self.tracking != 'serial')
        if products:
            products.product_instance = False
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    instance_serial_number_id = fields.Many2one('stock.production.lot', 'Serial Number', ondelete='set null', domain="[('product_id', '=', id)]")
    instance_current_location_id = fields.Many2one('stock.location', string="Current Location")

    @api.onchange('product_instance')
    def onchange_product_instance(self):
        if self.product_instance:
            self.tracking = 'serial'
            self.type = 'product'

    @api.onchange('tracking')
    def onchange_tracking(self):
        res = super(ProductProduct, self).onchange_tracking()
        products = self.filtered(lambda self: self.tracking and self.tracking != 'serial')
        if products:
            products.product_instance = False
        return res
