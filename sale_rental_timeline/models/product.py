# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_timeline_ids = fields.One2many('product.timeline', 'product_id', 'Time Lines')
