# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTimeline(models.Model):
    _name = 'product.timeline'
    _description = 'Product Timeline'

    res_model = fields.Char(
        require=True,
    )

    res_id = fields.Integer(
        require=True,
    )

    click_res_model = fields.Char(
        require=True,
    )

    click_res_id = fields.Integer(
        require=True,
    )

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
        ondelete='cascade',
        required=True,
    )

    order_name = fields.Char(
        'Order',
        require=True,
    )

    type = fields.Selection(
        string='Type',
        selection=[
            ('rental', 'Rental'),
            ('reserved', 'Reserved'),
        ],
    )

    has_clues = fields.Char(
        'Has Clues',
        compute='_compute_fields',
    )

    redline = fields.Boolean(
        'Redline',
    )

    product_tmpl_id = fields.Many2one(
        related='product_id.product_tmpl_id'
    )

    product_categ_id = fields.Many2one(
        related='product_id.categ_id',
    )

    name = fields.Char(
        'Name',
        compute='_compute_fields',
    )

    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        ondelete='set null',
        compute='_compute_fields',
    )

    partner_shipping_address = fields.Char(
        'Shipping address',
        compute='_compute_fields',
    )

    currency_id = fields.Many2one(
        'res.currency',
        compute='_compute_fields',
    )

    price_subtotal = fields.Monetary(
        currency_field='currency_id',
        field_digits=True,
        compute='_compute_fields',
    )

    number_of_days = fields.Integer(
        'Total days',
        compute='_compute_fields',
    )

    rental_period = fields.Char(
        compute='_compute_fields',
    )

    amount = fields.Char(
        compute='_compute_fields',
    )

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        compute='_compute_fields',
    )

    action_id = fields.Integer(
        compute='_compute_fields',
    )

    menu_id = fields.Integer(
        compute='_compute_fields',
    )

    _sql_constraints = [
        ('date_check', 'CHECK ((date_start <= date_end))', 'The start date must be anterior to the end date.'),
    ]

    @api.multi
    def _compute_fields(self):
        lang = self.env['res.lang'].search([('code', '=', self.env.user.lang)])
        for line in self:
            if line.res_model == 'sale.order.line':
                obj = self.env[line.res_model].browse(line.res_id)
                order_obj = obj.order_id
                line.name = _('R: %s') % order_obj.partner_id.name
                line.order_name = order_obj.name
                line.partner_id = order_obj.partner_id.id
                line.partner_shipping_address = order_obj.partner_shipping_id._display_address()

                line.warehouse_id = order_obj.warehouse_id.id
                line.currency_id = obj.currency_id.id
                line.price_subtotal = obj.price_subtotal
                line.number_of_days = obj.number_of_days
                line.rental_period = '{product_uom_qty} {product_uom}'.format(
                    product_uom_qty = int(obj.product_uom_qty),
                    product_uom = obj.product_uom.name,
                )
                currency = line.currency_id
                line.amount = '{price_subtotal} {currency}'.format(
                    price_subtotal = lang.format('%.2f', line.price_subtotal, grouping=True),
                    currency = currency.symbol,
                )
                line.has_clues = False

            line.action_id = self.env.ref('rental_base.action_rental_orders').id
            line.menu_id = self.env.ref('rental_base.menu_rental_root').id
