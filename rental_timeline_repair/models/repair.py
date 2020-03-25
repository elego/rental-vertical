# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    timeline_ids = fields.One2many(
        'product.timeline',
        compute='_compute_timeline_ids',
    )

    @api.multi
    def _compute_timeline_ids(self):
        for order in self:
            domain = [
                ('res_model', '=', order._name),
                ('res_id', '=', order.id),
            ]
            order.timeline_ids = self.env['product.timeline'].search(domain)

    @api.multi
    def _prepare_timeline_vals(self):
        self.ensure_one()
        return {
            'type': 'repair',
            'date_start': self.date_start,
            'date_end': self.date_deadline,
            'product_id': self.product_id.id,
            'order_name': self.name,

            'res_model': self._name,
            'res_id': self.id,
            'click_res_model': self._name,
            'click_res_id': self.id,
        }

    @api.multi
    def _create_product_timeline(self):
        self.ensure_one()
        if self.product_id.product_instance:
            vals = self._prepare_timeline_vals()
            self.env['product.timeline'].create(vals)

    @api.multi
    def _reset_timeline(self, vals):
        for order in self:
            if order.product_id.product_instance:
                if not order.timeline_ids:
                    raise exceptions.UserError(_('No found timelines.'))
                if vals.get('date_start', False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.date_start)
                    timelines[0].date_start = vals['date_start']
                if vals.get('date_deadline', False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.date_end, reverse=True)
                    timelines[0].date_end = vals['date_deadline']
                if vals.get('product_id', False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.product_id)
                    product = self.env['product.product'].browse(vals['product_id'])
                    timelines[0].product_id = product.id
                if vals.get('name', False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.order_name)
                    timelines[0].order_name = vals['name']
            else:
                raise exceptions.UserError(_('No found repaired product.'))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._create_product_timeline()
        return res

    @api.multi
    def write(self, vals):
        res = super(RepairOrder, self).write(vals)
        keys = {'date_start', 'date_deadline', 'product_id', 'name'}
        if keys.intersection(vals.keys()):
            reset_orders = self.browse([])
            date_start = vals.get('date_start', False)
            end_Date = vals.get('date_deadline', False)
            product_id = vals.get('product_id', False)
            name = vals.get('name', False)
            for order in self:
                if date_start and order.date_start != date_start:
                    reset_orders |= order
                if end_Date and order.date_deadline != end_Date:
                    reset_orders |= order
                if product_id and order.product_id != product_id:
                    reset_orders |= order
                if name and order.name != name:
                    reset_lines |= order
            reset_orders._reset_timeline(vals)
        return res

    @api.multi
    def unlink(self):
        res = super(RepairOrder, self).unlink()
        domain = [
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ]
        self.env['product.timeline'].search(domain).unlink()
        return res

    @api.multi
    def action_repair_cancel(self):
        """
            delete all time lines
        """
        for order in self:
            order.timeline_ids.unlink()
        res = super(RepairOrder, self).action_repair_cancel()
        return res
