# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    @api.multi
    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        for line in self:
            domain = [
                ('date_start', '<', line.date_end),
                ('date_end', '>', line.date_start),
                ('product_id', '=', line.product_id.id),
                ('product_id.product_instance', '=', True),
                ('id', '!=', line.id),
            ]
            lines = self.search_count(domain)
            if lines:
                raise exceptions.ValidationError(
                    _('You can not have 2 timelines that overlaps on the same day.'))

