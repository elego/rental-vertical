# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class CreateSaleTransRequest(models.TransientModel):
    _inherit = "create.sale.trans.request"

    @api.model
    def _prepare_line_vals(self, line):
        res = super()._prepare_line_vals(line)
        res["trans_return_shipment_plan_id"] = line.trans_return_shipment_plan_id.id
        return res

    def _prepare_shipment_plan_values(self, order):
        res = super()._prepare_shipment_plan_values(order)
        rental_order_type = self.env.ref("rental_base.rental_sale_type")
        if order.type_id.id == rental_order_type.id:
            src_address_id = res["from_address_id"]
            dest_address_id = res["to_address_id"]
            if self.env.context.get("shipment_plan_return", False):
                order_lines = self.origin_line_ids.mapped("order_line_id")
                return_note = order_lines.get_transport_details()
                res.update(
                    {
                        "plan_type": "rental",
                        "name": "Return Shipment Plan for %s" % order.name,
                        "initial_etd": order.default_end_date - timedelta(days=1),
                        "initial_eta": order.default_end_date,
                        "from_address_id": dest_address_id,
                        "to_address_id": src_address_id,
                        "note": return_note,
                    }
                )
            else:
                res.update(
                    {
                        "plan_type": "rental",
                        "initial_etd": order.default_start_date - timedelta(days=1),
                        "initial_eta": order.default_start_date,
                    }
                )
        return res

    # (override)
    def action_confirm(self):
        self.ensure_one()
        shipment_plan = False
        return_shipment_plan = False
        all_set, no_set = self._check_origin_lines()
        if all_set:
            shipment_plan = self.origin_line_ids[0].trans_shipment_plan_id
        elif no_set:
            vals = self._prepare_shipment_plan_values(self.order_id)
            shipment_plan = self.env["shipment.plan"].create(vals)
        else:
            raise execptions.UserError(_("No found suitable Shipment Plan."))
        shipment_plan.create_purchase_request(self.service_product_ids)
        rental_order_type = self.env.ref("rental_base.rental_sale_type")
        if self.order_id.type_id.id == rental_order_type.id:
            if all_set:
                return_shipment_plan = self.origin_line_ids[
                    0
                ].trans_return_shipment_plan_id
            elif no_set:
                vals_return = self.with_context(
                    shipment_plan_return=True
                )._prepare_shipment_plan_values(self.order_id)
                return_shipment_plan = self.env["shipment.plan"].create(vals_return)
            else:
                raise execptions.UserError(_("No found suitable Shipment Plan."))
            return_shipment_plan.create_purchase_request(self.service_product_ids)

        vals = {}
        if shipment_plan:
            vals["trans_shipment_plan_id"] = shipment_plan.id
        if return_shipment_plan:
            vals["trans_return_shipment_plan_id"] = return_shipment_plan.id
        self.origin_line_ids.mapped("order_line_id").write(vals)
        return shipment_plan, return_shipment_plan


class CreateSaleTransOriginLine(models.TransientModel):
    _inherit = "create.sale.trans.origin.line"

    trans_return_shipment_plan_id = fields.Many2one(
        "shipment.plan",
        string="Return Shipment Plan",
        related="order_line_id.trans_return_shipment_plan_id",
    )
