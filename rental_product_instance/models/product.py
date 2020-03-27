# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_instance_condition_type = fields.Selection(
        string="Show Instance Condition Type",
        selection=[
            ('hour', 'Hours'),
            ('km', 'Kilometers'),
        ],
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_instance = fields.Boolean(
        string='Product Instance',
        default=False,
        help='This product is a product instance, which can only have one unit in stock.',
    )

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

    instance_serial_number_id = fields.Many2one(
        'stock.production.lot',
        'Serial Number',
        ondelete='set null',
        domain="[('product_id', '=', id)]",
    )

    instance_current_location_id = fields.Many2one(
        'stock.location',
        string="Current Location",
    )
    instance_state = fields.Selection(string="State",
        selection=[
            ('available', 'Available'),
            ('rental', 'Rental'),
            ('reserved', 'Reserved'),
            ('maintenance', 'Maintenance'),
            ('repair', 'Repair'),
            ('delivery', 'Delivery'),
        ],
        compute="_compute_instance_state",
    )

    show_instance_condition_type = fields.Selection(
        string="Show Instance Condition Type",
        selection=[
            ('hour', 'Hours'),
            ('km', 'Kilometers'),
        ],
        related="categ_id.show_instance_condition_type",
    )

    instance_condition_hour = fields.Char(
        "Current Hours",
    )

    instance_condition_km = fields.Char(
        "Current Kilometers",
    )

    instance_condition_in_tree = fields.Char(
        "Current Kilmeter / Hours",
        compute="_compute_instance_condition_in_tree",
        store="True",
    )

    instance_condition_date = fields.Date(
        "Condition Date",
    )

    instance_next_service_date = fields.Date(
        "Next Service",
    )
    real_sale_price = fields.Float(string='Real Sale Price',
        help='This is the price at which the product instance was actually sold.')
    real_total_kilometers = fields.Float(string='Real Total Kilometers',
        help='This is the mileage the product instance had on sale.')
    real_total_hours = fields.Float(string='Real Total Hours',
        help='These are the total operating hours that the product instance had on sale.')
    real_total_rental_time = fields.Float(string='Real Total Rental Time',
        help='This is the total rental time for this product instance.')

    @api.multi
    @api.depends('instance_condition_hour', 'instance_condition_km')
    def _compute_instance_condition_in_tree(self):
        for record in self:
            record.instance_condition_in_tree = ''
            if record.show_instance_condition_type == 'hour':
                record.instance_condition_in_tree = \
                    record.instance_condition_hour
            elif record.show_instance_condition_type == 'km':
                record.instance_condition_in_tree = \
                    record.instance_condition_km

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
