# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    appointment_ids = fields.One2many(
        'product.appointment',
        'product_id',
        string="Appointments",
    )

    operating_appointment_ids = fields.One2many(
        'product.operating.appointment',
        'product_id',
        string="Operating Appointments",
    )
