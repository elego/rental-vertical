# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _run_rental_procurement(self, line, vals):
        location = line.order_id.warehouse_id.rental_out_location_id
        if line.trans_pr_needed:
            location = line.order_id.warehouse_id.transit_out_location_id
        self.env['procurement.group'].run(
            line.product_id.rented_product_id, line.rental_qty,
            line.product_id.rented_product_id.uom_id,
            location,
            line.name, line.order_id.name, vals)

    def _prepare_new_rental_procurement_values(self, group=False):
        res = super(SaleOrderLine, self)._prepare_new_rental_procurement_values(group=group)
        if self.trans_pr_needed:
            res['route_ids'] = self.order_id.warehouse_id.rental_transit_route_id
        else:
            res['route_ids'] = self.order_id.warehouse_id.rental_route_id
        return res
