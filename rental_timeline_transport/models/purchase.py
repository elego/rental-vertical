# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    timeline_ids = fields.One2many(
        'product.timeline',
        compute='_compute_timeline_ids',
    )

    @api.multi
    def _compute_timeline_ids(self):
        for line in self:
            domain = [
                ('res_model', '=', line._name),
                ('res_id', '=', line.id),
            ]
            line.timeline_ids = self.env['product.timeline'].search(domain)

    @api.multi
    def _prepare_timeline_vals(self):
        self.ensure_one()
        return {
            'type': 'delivery',
            'date_start': self.date_planned,
            'date_end': self.trans_origin_sale_line_id.start_date,
            'product_id': self.trans_origin_sale_line_id.product_id.rented_product_id.id,
            'order_name': self.order_id.name,

            'res_model': self._name,
            'res_id': self.id,
            'click_res_model': self.order_id._name,
            'click_res_id': self.order_id.id,
        }

    @api.multi
    def _create_product_timeline(self):
        self.ensure_one()
        transport_type = self.env.ref('rental_purchase_order_type.po_type_transport_order')
        transport_product = self.env.ref('rental_transport_purchase_request.product_transport')
        if self.product_id and self.product_id == transport_product:
            if self.order_id.order_type == transport_type:
                vals = self._prepare_timeline_vals()
                self.env['product.timeline'].create(vals)

    @api.multi
    def _reset_timeline(self, vals):
        for line in self:
            if line.product_id and line.product_id.product_instance:
                if not line.timeline_ids:
                    raise exceptions.UserError(_('No found timelines.'))
                if vals.get('date_planned', False):
                    timelines = sorted(line.timeline_ids, key=lambda l: l.date_start)
                    timelines[0].date_start = vals['date_planned']
                if vals.get('name', False):
                    timelines = sorted(line.timeline_ids, key=lambda l: l.name)
                    timelines[0].order_name = vals['name']
            else:
                raise exceptions.UserError(_('No found transport product.'))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._create_product_timeline()
        return res

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        keys = {'date_planned', 'name'}
        if keys.intersection(vals.keys()):
            reset_lines = self.browse([])
            start_date = vals.get('date_planned', False)
            name = vals.get('name', False)
            for line in self:
                if start_date and line.date_planned != start_date:
                    reset_lines |= line
                if name and line.name != name:
                    reset_lines |= line
            reset_lines._reset_timeline(vals)
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def write(self, vals):
        """
            delete all time lines if the order_type is not po_type_transport_order
        """
        transport_type = self.env.ref('rental_purchase_order_type.po_type_transport_order')
        for order in self:
            if order.order_type != transport_type:
                for line in order.order_line:
                    line.timeline_ids.unlink()
        res = super(PurchaseOrder, self).write(vals)
        return res

    @api.multi
    def button_cancel(self):
        """
            delete all time lines
        """
        for order in self:
            for line in order.order_line:
                line.timeline_ids.unlink()
        res = super(PurchaseOrder, self).action_cancel()
        return res
