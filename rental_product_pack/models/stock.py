# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    rental_pack_move_id = fields.Many2one("stock.move", "Rental Main Pack Move")
