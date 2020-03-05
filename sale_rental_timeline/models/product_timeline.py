# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.addons import decimal_precision as dp


RENTAL_TIMELINE_TYPES = [
    'rental',
    'reserved',
    'repair',
    'delivery',
]

class ProductTimeline(models.Model):
    _name = 'product.timeline'
    _description = 'Product Timeline'

    res_model = fields.Char()
    res_id = fields.Integer(oldname='sale_order_line_id')
    order_res_model = fields.Char()
    order_res_id = fields.Integer()

    date_start = fields.Datetime(
        'Date Start',
        require=True,
    )
    date_end = fields.Datetime(
        'Date End',
        require=True,
    )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        ondelete="cascade",
        required=True,
    )

    type = fields.Selection(
        string='Type',
        selection=[
            ('rental', 'Rental'),
            ('reserved', 'Reserved'),
            ('maintenance', 'Maintenance'),
            ('repair', 'Repair'),
            ('delivery', 'Delivery'),
        ],
    )
    termin = fields.Boolean(
        'Termin',
    )
    _maintenance = fields.Boolean(
        compute="_compute_fields",
    )
    maintenance = fields.Boolean(
        'Maintenance',
    )
    redline = fields.Boolean(
        'Redline',
    )

    product_tmpl_id = fields.Many2one(
        related="product_id.product_tmpl_id"
    )

    product_categ_id = fields.Many2one(
        related="product_id.categ_id",
    )
    name = fields.Char(
        'Name',
        compute="_compute_fields",
    )
    order_name = fields.Char(
        'Order',
        compute="_compute_fields",
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        ondelete="set null",
        compute="_compute_fields",
    )
    partner_shipping_address = fields.Char(
        "Shipping address",
        compute="_compute_fields",
    )
    currency_id = fields.Many2one(
        'res.currency',
        compute="_compute_fields",
    )
    price_subtotal = fields.Monetary(
        currency_field='currency_id',
        field_digits=True,
        compute="_compute_fields",
    )
    number_of_days = fields.Integer(
        'Total days',
        compute="_compute_fields",
    )
    rental_period = fields.Char(
        compute="_compute_fields",
    )
    amount = fields.Char(
        compute="_compute_fields",
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        compute="_compute_fields",
    )

    action_id = fields.Integer(
        compute="_compute_fields",
    )
    menu_id = fields.Integer(
        compute="_compute_fields",
    )

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end))", "The start date must be anterior to the end date."),
    ]

    @api.multi
    def _compute_fields(self):
        for line in self:
            obj = self.env[line.res_model].browse(line.res_id)
            order_obj = self.env[line.order_res_model].browse(line.order_res_id)

            if line.res_model == 'sale.order.line':
                line.name = _('Rental: %s') % order_obj.partner_id.name
                line.order_name = order_obj.name
                line.partner_id = order_obj.partner_id.id
                line.partner_shipping_address = order_obj.partner_shipping_id._display_address()

                line.warehouse_id = order_obj.warehouse_id.id
                line.currency_id = obj.currency_id.id
                line.price_subtotal = obj.price_subtotal
                line.number_of_days = obj.number_of_days
                line.rental_period = "{product_uom_qty} {product_uom}".format(
                    product_uom_qty=int(obj.product_uom_qty),
                    product_uom=obj.product_uom.name,
                )
                line.amount = "{price_subtotal} {currency}".format(
                    price_subtotal=line.price_subtotal,
                    currency=line.currency_id.name,
                )

            elif line.res_model == 'repair.order':
                line.name = _('R: %s') % obj.partner_id.name
                line.order_name = obj.name
                line.partner_id = obj.partner_id.id
                line.partner_shipping_address = obj.address_id._display_address()
                line.amount = "{total} {currency}".format(
                    total=obj.amount_untaxed,
                    currency=self.env.user.company_id.currency_id.name,
                )

            _maintenance_domain = [
                ('type', '=', 'repair'),
                ('product_id', '=', line.product_id.id),
                ('date_start', '>=', line.date_start),
                ('date_end', '<=', line.date_end),
            ]
            line._maintenance = False if line.type == 'repair' and not line.maintenance else bool(self.search(_maintenance_domain))
            line.action_id = self.env.ref('rental_base.action_rental_orders').id
            line.menu_id = self.env.ref('rental_base.menu_rental_root').id



#    @api.multi
#    def action_view_record(self):
#        self.ensure_one()
#        if self.type in RENTAL_TIMELINE_TYPES:
#            return self._action_view_sale_order(self.sale_order_line_id.order_id)
#        return super(ProductTimeline, self).action_view_record()
#
#    @api.multi
#    def _action_view_sale_order(self, order):
#        self.ensure_one()
#        if not order:
#            raise exceptions.UserError(_('No found referenced Sale Order'))
#        view_id = self.env.ref("sale.order_form").id
#        return {
#            'type': 'ir.actions.act_window',
#            'name': _('Sale Order'),
#            'target': 'new',
#            'view_mode': "form",
#            'view_id': view_id,
#            'res_model': 'sale.order',
#            'res_id': order.id,
#            }
