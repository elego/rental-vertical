# Part of rental-vertical See LICENSE file for full copyright and licensing details.

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
    instance_state = fields.Selection(string="State",
        selection=[
            ('available', 'Available'),
            ('rental', 'Rental'),
            ('reserved', 'Reserved'),
            ('maintenance', 'Maintenance'),
            ('repair', 'Repair'),
            ('delivery', 'Delivery'),
        ], compute="_compute_instance_state")
    instance_current_condition = fields.Char("Current Hours / Kilometers")
    instance_next_service_date = fields.Date("Next Service")

    def _compute_instance_state(self):
        timeline_obj = self.env['product.timeline']
        today = fields.Date.today()
        for product in self:
            product.instance_state = 'available'
            timelines = timeline_obj.search([
                ('product_id', '=', product.id),
                ('date_start', '<=', today),
                ('date_end', '>=', today),
            ])
            if timelines:
                product.instance_state = timelines[0].type

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
