# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


RENTAL_TIMELINE_TYPES = ['rental', 'reserved']


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
    date_start = fields.Datetime('Date Start', required=True)
    date_end = fields.Datetime('Date End', required=True)
    title = fields.Char(compute='_compute_title')

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

#    @api.multi
#    def action_view_record(self):
#        """
#        Override this method to show the form view of the referenced record.
#        """
#        raise exceptions.ValidationError(_('No found implementation.'))

    @api.multi
    @api.depends('name')
    def _compute_title(self):
        for rec in self:
            rec.title = rec.name
