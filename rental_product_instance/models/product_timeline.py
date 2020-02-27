# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, _


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    @api.multi
    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        for line in self:
            if line.type in ['rental', 'reserved']:
                domain = [
                    ('date_start', '<', line.date_end),
                    ('date_end', '>', line.date_start),
                    ('product_id', '=', line.product_id.id),
                    ('product_id.product_instance', '=', True),
                    ('type', 'in', ['rental', 'reserved']),
                    ('id', '!=', line.id),
                ]
                lines = self.search_count(domain)
                if lines:
                    raise exceptions.ValidationError(
                        _('You can not have 2 timelines that overlaps on the same day.'))

