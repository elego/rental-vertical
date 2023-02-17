# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class InstanceOperatingData(models.Model):
    _name = "instance.operating.data"
    _description = "Instance Operating Data"
    _order = "date desc"

    instance_id = fields.Many2one(
        "product.product",
        string="Product Instance",
        required=True,
    )

    operating_data = fields.Float(
        string="Operating Data",
        required=True,
    )

    date = fields.Datetime(
        string="Date",
        required=True,
    )
