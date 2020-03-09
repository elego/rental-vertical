# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    product_instance_state = fields.Selection(
        related='product_id.instance_state',
    )

    product_instance_next_service_date = fields.Date(
        related='product_id.instance_next_service_date',
    )

    product_instance_current_location_id = fields.Many2one(
        related='product_id.instance_current_location_id',
    )

    product_instance_serial_number_id = fields.Many2one(
        related='product_id.instance_serial_number_id',
    )

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
                    msg = _('You can not have 2 timelines that overlaps on the same day.')
                    raise exceptions.ValidationError(msg)

