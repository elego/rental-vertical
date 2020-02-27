# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)

#TODO We need to change the function _action_launch_stock_rule in sale_rental module
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    planned_in_location_id = fields.Many2one('stock.location', string="Planned Source Location")

#    def _set_planned_rental_in_location(self):
#        self.ensure_one()
#        rental_in_location = self.order_id.warehouse_id.rental_in_location_id
#        #rental_out_location = self.order_id.warehouse_id.rental_out_location_id
#        planned_in_location_id = self.planned_in_location_id or rental_in_location.id
#        #planned_out_location_id = self.planned_out_location_id or rental_out_location.id
#        for move in self.move_ids:
#            if move.location_id.id == rental_in_location.id and planned_in_location_id != rental_in_location.id:
#                move.location_id = planned_in_location_id
#                if len(move.picking_id.move_lines) == 1:
#                    move.picking_id.location_id = planned_in_location_id
#                else:
#                    move.picking_id = False
#                    move._assign_picking()

    def _run_rental_procurement(self, line, vals):
        location = line.order_id.warehouse_id.rental_out_location_id
        if line.route_id and line.route_id == line.order_id.warehouse_id.rental_transit_route_id:
            location = line.order_id.warehouse_id.transit_out_location_id
        self.env['procurement.group'].run(
            line.product_id.rented_product_id, line.rental_qty,
            line.product_id.rented_product_id.uom_id,
            location,
            line.name, line.order_id.name, vals)
        #line._set_planned_rental_in_location()

    def _prepare_new_rental_procurement_values(self, group=False):
        res = super(SaleOrderLine, self)._prepare_new_rental_procurement_values(group=group)
        if self.planned_in_location_id:
            res['planned_in_location_id'] = self.planned_in_location_id.id
        if self.route_id and self.route_id == self.order_id.warehouse_id.rental_transit_route_id:
            res['route_ids'] = self.order_id.warehouse_id.rental_transit_route_id
        return res
