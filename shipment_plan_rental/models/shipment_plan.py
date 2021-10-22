# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    plan_type = fields.Selection(
        selection_add=[("rental", "Rental")],
    )

    origin_return_sale_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="trans_return_shipment_plan_id",
        string="Origin Return Sale Order Lines",
    )

    @api.multi
    def _get_transport_pr_name(self):
        self.ensure_one()
        if self.env.context.get("rental_return", False):
            return _("Inbound transport for %s") % self.origin
        return _("Outbound transport for %s") % self.origin


