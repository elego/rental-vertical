# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(
        selection_add=[("internal", "Internal Picking"), ("sale", "Sale")],
    )

    origin_sale_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="trans_shipment_plan_id",
        string="Origin Sale Order Lines",
        copy=False,
    )

    sale_id = fields.Many2one(
        comodel_name="sale.order",
        string="Origin Sale Order",
        compute="_compute_sale_id",
    )

    move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="shipment_plan_id",
        copy=False,
    )

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        compute="_compute_picking_ids",
    )

    picking_count = fields.Integer(
        compute="_compute_picking_ids",
    )

    @api.depends("origin_sale_line_ids")
    def _compute_sale_id(self):
        for record in self:
            if record.origin_sale_line_ids:
                record.sale_id = record.origin_sale_line_ids[0].order_id

    @api.depends("move_ids")
    def _compute_picking_ids(self):
        for record in self:
            pickings = self.env["stock.picking"].browse()
            for move in record.move_ids:
                if move.picking_id:
                    pickings |= move.picking_id
            record.picking_ids = pickings
            record.picking_count = len(pickings)

    def action_view_pickings(self):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        action["domain"] = [("id", "in", self.picking_ids.ids)]
        return action
