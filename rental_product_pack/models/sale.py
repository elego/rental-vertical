# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            out_pickings = order.picking_ids.filtered(lambda x: x.picking_type_id.code == "outgoing")
            in_pickings = order.picking_ids.filtered(lambda x: x.picking_type_id.code == "incoming")
            for picking in out_pickings:
                for move in picking.move_ids_without_package:
                    if move.product_id and move.product_id.pack_ok:
                        for line in move.product_id.pack_line_ids:
                            new_move = move.copy({
                                'product_id': line.product_id.id,
                                'product_uom_qty': move.product_uom_qty * line.quantity,
                                'rental_pack_move_id': move.id,
                                'picking_id': move.picking_id and move.picking_id.id or False,
                            })
            out_pickings.action_confirm()
            in_pickings.action_confirm()

        return res
