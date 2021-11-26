# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class CreateSaleTransRequest(models.TransientModel):
    _inherit = "create.sale.trans.request"

    def _prepare_shipment_plan_values(self, order):
        res = super()._prepare_shipment_plan_values(order)
        rental_order_type = self.env.ref("rental_base.rental_sale_type")
        if order.type_id.id == rental_order_type.id:
            if self.env.context.get("shipment_plan_return", False):
                res.update(
                    {
                        "location_id": order.partner_shipping_id.rental_onsite_location_id.id,
                        "location_dest_id": order.warehouse_id.rental_in_location_id.id,
                    }
                )
            else:
                res.update(
                    {
                        "location_id": order.warehouse_id.rental_in_location_id.id,
                        "location_dest_id": order.partner_shipping_id.rental_onsite_location_id.id,
                    }
                )
        return res

    # (override)
    def action_confirm(self):
        self.ensure_one()
        if (
            self.order_id.partner_shipping_id
            and not self.order_id.partner_shipping_id.rental_onsite_location_id
        ):
            self.order_id.create_and_set_rental_onsite_location_route()
        return super().action_confirm()
