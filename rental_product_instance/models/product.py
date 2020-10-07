# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression


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
    instance_state = fields.Selection(
        string="State",
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
        store=True,
    )

    instance_condition_hour = fields.Char(
        string="Current Hours",
        compute="_compute_instance_condition",
    )

    instance_condition_km = fields.Char(
        string="Current Kilometers",
        compute="_compute_instance_condition",
    )

    instance_condition_in_tree = fields.Char(
        string="Current Operating Data",
        compute="_compute_instance_condition",
    )

    instance_condition_date = fields.Date(
        string="Condition Date",
        compute="_compute_instance_condition",
    )

    instance_next_service_date = fields.Date(
        string="Next Service",
    )

    real_sale_price = fields.Float(
        string='Real Sale Price',
        help='This is the price at which the product instance was actually sold.'
    )

    real_total_kilometers = fields.Float(
        string='Real Total Kilometers',
        help='This is the mileage the product instance had on sale.'
    )

    real_total_hours = fields.Float(
        string='Real Total Hours',
        help='These are the total operating hours that the product instance had on sale.'
    )

    real_total_rental_time = fields.Float(
        string='Real Total Rental Time',
        help='This is the total rental time for this product instance.'
    )

    instance_operating_data_ids = fields.One2many(
        'instance.operating.data',
        'instance_id',
        string="Operating Data"
    )

    @api.multi
    def _compute_instance_condition(self):
        for record in self:
            record.instance_condition_km = ''
            record.instance_condition_hour = ''
            record.instance_condition_in_tree = ''
            record.instance_condition_date = False
            for o_data in record.instance_operating_data_ids:
                if not record.instance_condition_date:
                    record.instance_condition_date = o_data.date
                    record.instance_condition_in_tree = str(o_data.operating_data)
                if o_data.date > record.instance_condition_date:
                    record.instance_condition_date = o_data.date
                    record.instance_condition_in_tree = str(o_data.operating_data)
            if record.show_instance_condition_type == 'hour':
                record.instance_condition_hour = \
                    record.instance_condition_in_tree
            elif record.show_instance_condition_type == 'km':
                record.instance_condition_km = \
                    record.instance_condition_in_tree

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

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        res = super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid
        )
        args = args or []
        if name:
            domain = [
                '|',
                ('instance_serial_number_id.name', operator, name),
                ('license_plate', operator, name),
            ]
            record_ids = self._search(
                expression.AND([domain, args]),
                limit=limit,
                access_rights_uid=name_get_uid
            )
            if record_ids:
                res2 = self.browse(record_ids).name_get()
                return list(set(res + res2))
        return res

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

    @api.multi
    def action_view_operating_data(self):
        self.ensure_one()
        action = self.env.ref('rental_product_instance.action_instance_operating_data').read([])[0]
        action['context'] = {'default_instance_id': self.id, 'search_default_instance_id': self.id}
        return action
