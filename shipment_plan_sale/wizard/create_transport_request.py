# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class CreateSaleTransRequest(models.TransientModel):
    _name = "create.sale.trans.request"
    _description = "Create Transport Purchase Request for Sale Order"

    origin_line_ids = fields.One2many(
        "create.sale.trans.origin.line",
        "wizard_id",
        string="Order Lines",
    )
    service_product_ids = fields.Many2many(
        "product.product",
        string="Services",
        domain="[('is_transport', '=', True)]",
    )
    transport_service_type = fields.Selection(
        [
            ("po", "Purchase Order"),
            ("pr", "Purchase Requisition"),
        ],
        default="po",
        string="Request type",
        help="The transport request type defines if a purchase order or a call for tender is created when requesting a transport within an order.",
    )
    order_id = fields.Many2one(
        "sale.order",
        "Sale Order",
    )

    @api.multi
    def _check_origin_lines(self):
        self.ensure_one()
        order_lines = self.origin_line_ids.mapped("order_line_id")
        all_set = all([l.trans_shipment_plan_id for l in order_lines])
        no_set = all([not l.trans_shipment_plan_id for l in order_lines])
        if not all_set and not no_set:
            raise exceptions.UserError(
                _("Some of the selected sale order lines do not have a Shipment Plan.")
            )
        elif all_set:
            # check if all the origin line was assigned to the same shipment plan
            shipment_plan = False
            order_lines = self.origin_line_ids.mapped("order_line_id")
            for line in order_lines:
                if not shipment_plan:
                    shipment_plan = line.trans_shipment_plan_id
                if shipment_plan.id != line.trans_shipment_plan_id.id:
                    raise exceptions.UserError(
                        _(
                            "You can not create the purchase request for sale order lines with different Shipment Plan."
                        )
                    )
            if len(shipment_plan.origin_sale_line_ids) != len(order_lines):
                raise exceptions.UserError(
                    _("All the order lines in shipment plan should be selected.")
                )
        return all_set, no_set

    @api.model
    def _prepare_line_vals(self, line):
        res = {
            "order_line_id": line.id,
            "product_id": line.product_id.id,
            "product_uom_qty": line.product_uom_qty,
            "product_uom": line.product_uom.id,
            "start_date": line.start_date,
            "end_date": line.end_date,
            "trans_shipment_plan_id": line.trans_shipment_plan_id.id,
        }
        return res

    @api.model
    def default_get(self, fields):
        res = super(CreateSaleTransRequest, self).default_get(fields)
        order_id = self.env.context.get("active_id", False)
        order = self.env["sale.order"].browse(order_id)
        order_lines = order.order_line.filtered(lambda l: l.trans_pr_needed)
        origin_line_ids = []
        for line in order_lines:
            line_vals = self._prepare_line_vals(line)
            origin_line_ids.append((0, 0, line_vals))
        res.update({"order_id": order.id, "origin_line_ids": origin_line_ids})
        return res

    def _prepare_shipment_plan_values(self, order):
        order = self.order_id
        src_address_id = self.env.user.company_id.with_context(show_address=True).id
        dest_address_id = order.partner_shipping_id.with_context(show_address=True).id
        order_lines = self.origin_line_ids.mapped("order_line_id")
        note = order_lines.get_transport_details()
        dangerous_goods = any([l.dangerous_goods for l in order.order_line])
        res = {
            "name": "Shipment Plan for %s" % order.name,
            "plan_type": "sale",
            "from_address_id": src_address_id,
            "to_address_id": dest_address_id,
            "note": note,
            "initial_etd": order.date_order - timedelta(days=1),
            "initial_eta": order.date_order,
            "origin": order.name,
            "origin_sale_line_ids": [(6, 0, order_lines.ids)],
            "dangerous_goods": dangerous_goods,
        }
        return res

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        shipment_plan = False
        all_set, no_set = self._check_origin_lines()
        if all_set:
            shipment_plan = self.origin_line_ids[0].trans_shipment_plan_id
        elif no_set:
            vals = self._prepare_shipment_plan_values(self.order_id)
            shipment_plan = self.env["shipment.plan"].create(vals)
            self.origin_line_ids.mapped("order_line_id").write(
                {
                    "trans_shipment_plan_id": shipment_plan.id,
                }
            )
        else:
            raise execptions.UserError(_("No found suitable Shipment Plan."))
        shipment_plan.create_purchase_request(
            self.service_product_ids, self.transport_service_type
        )
        return shipment_plan

    @api.onchange("service_product_ids")
    def onchange_service_product_ids(self):
        if self.service_product_ids:
            self.transport_service_type = self.service_product_ids[0].transport_service_type

class CreateSaleTransOriginLine(models.TransientModel):
    _name = "create.sale.trans.origin.line"
    _description = "Original Sale Order Line"

    wizard_id = fields.Many2one(
        "create.sale.trans.request",
    )
    order_line_id = fields.Many2one("sale.order.line")
    product_id = fields.Many2one(
        "product.product",
        related="order_line_id.product_id",
    )
    product_uom_qty = fields.Float(
        "Quantity",
        related="order_line_id.product_uom_qty",
    )
    product_uom = fields.Many2one(
        "uom.uom",
        string="UOM",
        related="order_line_id.product_uom",
    )
    start_date = fields.Date(
        "Start Date",
    )
    end_date = fields.Date(
        "End Date",
    )
    trans_shipment_plan_id = fields.Many2one(
        "shipment.plan",
        string="Shipment Plan",
        related="order_line_id.trans_shipment_plan_id",
    )
