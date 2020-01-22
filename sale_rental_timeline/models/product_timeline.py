# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


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
    product_id = fields.Many2one('product.product', 'Equipment', required=True, ondelete="cascade")
    partner_id = fields.Many2one('res.partner', 'Partner', ondelete="set null")
    type = fields.Selection(string='Type', selection=[
        ('rental', 'Rental'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('delivery', 'Delivery'),
    ])
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", ondelete="cascade")
    sale_order_id = fields.Many2one(related="sale_order_line_id.order_id")

    date_start = fields.Datetime('Date Start', required=True)
    date_end = fields.Datetime('Date End', required=True)

    currency_id = fields.Many2one(related="sale_order_line_id.currency_id")
    price_subtotal = fields.Monetary(related="sale_order_line_id.price_subtotal", currency_field='currency_id', field_digits= True)

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end))", "The start date must be anterior to the end date."),
    ]


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
