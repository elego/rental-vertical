# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class InstanceOperatingData(models.Model):
    _name = 'instance.operating.data'

    instance_id = fields.Many2one(
        'product.product',
        string="Instance",
    )

    operating_data = fields.Char(
        string='Current Kilmeter / Hours',
    )

    date = fields.Date(
        string='Date',
    )
