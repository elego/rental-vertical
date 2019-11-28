# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


class ProductTimeline(models.Model):
    _name = 'product.timeline'
    _description = 'Product Timeline'

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', 'Equipment')
    partner_id = fields.Many2one('res.partner', 'Partner')
    type = fields.Selection(string='Type', selection=[
        ('rental', 'Rental'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('delivery', 'Delivery'),
    ])
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end))", "The start date must be anterior to the end date."),
    ]

    @api.multi
    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        for line in self:
            domain = [
                ('date_start', '<', line.date_end),
                ('date_end', '>', line.date_start),
                ('product_id', '=', line.product_id.id),
                ('id', '!=', line.id),
            ]
            lines = self.search_count(domain)
            if lines:
                raise exceptions.ValidationError(
                    _('You can not have 2 timelines that overlaps on the same day.'))
