# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, _
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

    name = fields.Char('Name')
    termin = fields.Boolean('Termin')
    maintenance = fields.Boolean('Maintenance')
    redline = fields.Boolean('Redline')
    product_id = fields.Many2one('product.product', 'Product', required=True, ondelete="cascade")
    product_tmpl_id = fields.Many2one(related="product_id.product_tmpl_id")
    categ_id = fields.Many2one(related="product_tmpl_id.categ_id")
    partner_id = fields.Many2one('res.partner', 'Partner', ondelete="set null")
    partner_shipping_address = fields.Char("Shipping address")
    type = fields.Selection(string='Type', selection=[
        ('rental', 'Rental'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('delivery', 'Delivery'),
    ])
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", ondelete="cascade")
    sale_order_id = fields.Many2one(related="sale_order_line_id.order_id")

    date_start = fields.Date('Date Start', required=True)
    date_end = fields.Date('Date End', required=True)

    currency_id = fields.Many2one(related="sale_order_line_id.currency_id")
    price_subtotal = fields.Monetary(related="sale_order_line_id.price_subtotal", currency_field='currency_id', field_digits= True)

    number_of_days = fields.Integer('Total days', related="sale_order_line_id.number_of_days")
    product_uom_qty = fields.Float('Rental days', related="sale_order_line_id.product_uom_qty")
    product_uom = fields.Many2one(related="sale_order_line_id.product_uom")
    rental_period = fields.Char(compute="_compute_rental_period_and_amount")
    amount = fields.Char(compute="_compute_rental_period_and_amount")
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    action_id = fields.Integer('Action')
    menu_id = fields.Integer('Menu')

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end))", "The start date must be anterior to the end date."),
    ]

    @api.multi
    def _compute_rental_period_and_amount(self):
        for line in self:
            line.rental_period = "{product_uom_qty} {product_uom}".format(
                product_uom_qty=int(line.product_uom_qty),
                product_uom=line.product_uom.name,
            )
            line.amount = "{price_subtotal} {currency}".format(
                price_subtotal=line.price_subtotal,
                currency=line.currency_id.name,
            )


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
