# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    rental_pack_move_id = fields.Many2one('stock.move', 'Rental Main Pack Move')
