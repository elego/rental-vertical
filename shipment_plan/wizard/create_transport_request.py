# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class CreateTransRequest(models.TransientModel):
    _name = "create.trans.request"
    _description = "Create Transport Purchase Request"

    service_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Services",
        domain="[('is_transport', '=', True)]",
    )

    shipment_plan_id = fields.Many2one(
        comodel_name="shipment.plan",
        string="Shipment Plan",
    )

    transport_service_type = fields.Selection(
        selection=[
            ("po", "Purchase Order"),
            ("pr", "Purchase Requisition"),
        ],
        string="Request type",
        help="The transport request type defines if a purchase "
             "order or a call for tender is created when requesting "
             "a transport within an order.",
    )

    @api.model
    def default_get(self, fields):
        res = {}
        active_id = self.env.context.get("active_id")
        shipment_plan = self.env["shipment.plan"].browse(active_id)
        res.update(
            {
                "shipment_plan_id": shipment_plan.id,
            }
        )
        return res

    def action_confirm(self):
        self.ensure_one()
        self.shipment_plan_id.create_purchase_request(
            self.service_product_ids, self.transport_service_type
        )

    @api.onchange("service_product_ids")
    def onchange_service_product_ids(self):
        if self.service_product_ids:
            self.transport_service_type = self.service_product_ids[0].transport_service_type
