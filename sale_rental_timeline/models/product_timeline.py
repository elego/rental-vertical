# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _

#from odoo.addons.swrent_product_extension.models.product_timeline import RENTAL_TIMELINE_TYPES

class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", ondelete="cascade")

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
