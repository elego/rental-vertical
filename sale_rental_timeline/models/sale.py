# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    timeline_ids = fields.One2many('product.timeline', 'sale_order_line_id', 'Timelines')

    @api.model
    def _prepare_timeline_vals(self, line):
        return {
            'name': _('Rental: %s') %self.order_id.partner_id.name,
            'product_id': self.product_id.rented_product_id.id,
            'sale_order_line_id': line.id,
            'type': 'reserved',
            'date_start': self.start_date,
            'date_end': self.end_date,
            'partner_id': self.order_id.partner_id.id,
        }

    @api.multi
    def _create_product_timeline(self):
        self.ensure_one()
        if self.product_id.rented_product_id and self.product_id.rented_product_id.product_instance:
            if self.rental_type in ['new_rental', 'rental_extension']:
                vals = self._prepare_timeline_vals(self)
                self.write({'timeline_ids': [(0, 0, vals)]})
            
    @api.multi
    def _reset_timeline(self, vals):
        for line in self:
            if line.product_id.rented_product_id and line.product_id.rented_product_id.product_instance:
                if not line.timeline_ids:
                    raise exceptions.UserError(_('No found timelines.'))
                if vals.get('start_date', False):
                    timelines = sorted(line.timeline_ids, key=lambda l: l.date_start)
                    timelines[0].date_start = vals['start_date']
                if vals.get('end_date', False):
                    timelines = sorted(line.timeline_ids, key=lambda l: l.date_end, reverse=True)
                    timelines[0].date_end = vals['end_date']
            else:
                raise exceptions.UserError(_('No found rented product.'))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._create_product_timeline()
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        if 'start_date' in vals or 'end_date' in vals:
            reset_lines = self.browse([])
            start_date = vals.get('start_date', False)
            end_Date = vals.get('end_date', False)
            for line in self:
                if start_date and line.start_date != start_date:
                    reset_lines |= line
                if end_Date and line.end_date != end_Date:
                    reset_lines |= line
            reset_lines._reset_timeline(vals)
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        """
            delete all time lines
        """
        for order in self:
            for line in order.order_line.filtered(
                    lambda l: l.rental_type == 'rental_extension' or
                    l.rental_type == 'new_rental'):
                line.timeline_ids.unlink()
        res = super(SaleOrder, self).action_cancel()
        return res

    def action_confirm(self):
        """
            change type of time lines
        """
        for order in self:
            for line in order.order_line.filtered(
                    lambda l: l.rental_type == 'rental_extension' or
                    l.rental_type == 'new_rental'):
                line.timeline_ids.write({'type': 'rental'})
        res = super(SaleOrder, self).action_confirm()
        return res
