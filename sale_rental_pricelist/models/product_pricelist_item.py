# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    day_item_id = fields.Many2one('product.product', string='Rental Service (Day)')
    month_item_id = fields.Many2one('product.product', string='Rental Service (Month)')
    hour_item_id = fields.Many2one('product.product', string='Rental Service (Hour)')