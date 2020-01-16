# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    rented_product_id = fields.Many2one('product.product', string='Rental Service')