# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dangerous_goods = fields.Boolean(
        string="Dangerous Goods",
    )

    trans_pr_needed = fields.Boolean(
        string="Transport Request",
        compute="_compute_trans_pr_needed",
        help="If set, the salesperson can create a transport "
             "request or call for tender for the chosen products "
             "in order to find a carrier delivering it.",
    )

    trans_shipment_plan_id = fields.Many2one(
        comodel_name="shipment.plan",
        string="Shipment Plan",
        ondelete="set null",
        copy=False,
    )

    trans_requisition_line_ids = fields.Many2many(
        comodel_name="purchase.requisition.line",
        related="trans_shipment_plan_id.trans_requisition_line_ids",
        string="Transfer Requisition Line",
    )

    trans_purchase_line_ids = fields.Many2many(
        comodel_name="purchase.order.line",
        related="trans_shipment_plan_id.trans_purchase_line_ids",
        string="Transfer Purchase Line",
    )

    @api.multi
    def _compute_trans_pr_needed(self):
        for line in self:
            line.trans_pr_needed = False
            if line.order_id.incoterm and line.order_id.incoterm.trans_pr_needed:
                if not line.product_id:
                    continue
                if line.product_id.trans_purchase_request:
                    line.trans_pr_needed = True

    @api.multi
    def get_transport_details(self):
        order = self[0].order_id
        res = ""
        src_address = self.env.user.company_id.partner_id._display_address()
        dest_address = order.partner_shipping_id._display_address()
        res += _("Incoterm: %s \n") % order.incoterm.name
        for line in self:
            res += "%s: %s %s \n" % (
                line.product_id.name,
                line.product_uom_qty,
                line.product_id.uom_id.name,
            )
        res += _("Date: %s \n") % order.date_order
        res += _("Source Address: \n %s \n\n") % src_address
        res += _("Destination Address: \n %s \n\n") % dest_address
        return res

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id=group_id)
        if self.trans_shipment_plan_id:
            res["shipment_plan_id"] = self.trans_shipment_plan_id.id
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _default_transport_cost_type(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("stock.transport_cost_type")
        )

    trans_pr_needed = fields.Boolean(
        string="Transport Request",
        compute="_compute_trans_pr_needed",
        help="If set, the salesperson can create a transport "
             "request or call for tender for the chosen products "
             "in order to find a carrier delivering it.",
    )

    transport_cost_type = fields.Selection(
        selection=[
            ("single", "Single Position"),
            ("multi", "Multi Positions")
        ],
        default=_default_transport_cost_type,
        help="Choosing the cost type 'Multi Positions' the transport "
             "purchase order or call for tender can contain several lines "
             "for the different costs related to the transport, "
             "e.g. the transport costs itself and several charges. "
             "You can define the appropriate transport services when "
             "creating a new transport request.\n"
             "Choosing the cost type 'Single Position’ the transport "
             "request will only consist of one line with all costs.",
    )

    trans_shipment_plan_ids = fields.Many2many(
        comodel_name="shipment.plan",
        compute="_compute_shipment_plans",
    )

    trans_pr_ids = fields.One2many(
        comodel_name="purchase.requisition",
        string="Tenders",
        compute="_compute_shipment_plans",
    )

    trans_po_ids = fields.One2many(
        comodel_name="purchase.order",
        string="RFQs",
        compute="_compute_shipment_plans",
    )
    trans_shipment_plan_count = fields.Integer(
        compute="_compute_shipment_plans",
    )

    trans_pr_count = fields.Integer(
        compute="_compute_shipment_plans",
    )

    trans_po_count = fields.Integer(
        compute="_compute_shipment_plans",
    )

    @api.multi
    @api.depends(
        "order_line",
        "order_line.trans_shipment_plan_id",
        "order_line.trans_shipment_plan_id.trans_purchase_line_ids",
        "order_line.trans_shipment_plan_id.trans_requisition_line_ids",
    )
    def _compute_shipment_plans(self):
        for order in self:
            trans_sps = self.env["shipment.plan"]
            trans_prs = self.env["purchase.requisition"]
            trans_pos = self.env["purchase.order"]
            for line in order.order_line:
                trans_sps |= line.trans_shipment_plan_id
                for pr_line in line.trans_shipment_plan_id.trans_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_shipment_plan_id.trans_purchase_line_ids:
                    trans_pos |= po_line.order_id
            order.trans_shipment_plan_ids = trans_sps
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
            order.trans_shipment_plan_count = len(trans_sps.ids)
            order.trans_pr_count = len(trans_prs.ids)
            order.trans_po_count = len(trans_pos.ids)

    @api.multi
    def _compute_trans_pr_needed(self):
        for order in self:
            order.trans_pr_needed = False
            # set true if one of the sale order line need the transport purchase request
            for line in order.order_line:
                if not line.product_id:
                    continue
                if line.trans_pr_needed:
                    order.trans_pr_needed = True
                    break

    @api.model
    def _prepare_cost_line(self, product, qty, uom, price, name):
        return {
            "product_id": product.id,
            "product_uom_qty": qty,
            "product_uom": uom.id,
            "price_unit": price,
            "name": name,
        }

    @api.multi
    def action_create_trans_cost(self):
        self.ensure_one()
        price_unit = sum(
            [p.amount_untaxed for p in self.trans_po_ids if p.selected_in_order]
        )
        margin = 0
        if price_unit == 0:
            raise exceptions.UserError(
                _(
                    "You need to select a transport purchase RFQ for this sale order first."
                )
            )
        if self.transport_cost_type == "single":
            cost = 0
            name = ""
            for p in self.trans_po_ids:
                if p.selected_in_order:
                    for pol in p.order_line:
                        margin = pol.product_id.transport_sales_margin
                        cost += pol.price_unit * (1 + (margin / 100))
                        name += "%s\n" % pol.product_id.name
            product_id = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("stock.transport_cost_product_id")
            )
            product_transport_cost = self.env["product.product"].browse(int(product_id))
            cost_line_vals = self._prepare_cost_line(
                product_transport_cost, 1, self.env.ref("uom.product_uom_unit"), cost, name,
            )
            self.write({"order_line": [(0, 0, cost_line_vals)]})
        elif self.transport_cost_type == "multi":
            order_line_vals = []
            for p in self.trans_po_ids:
                if p.selected_in_order:
                    for pol in p.order_line:
                        margin = pol.product_id.transport_sales_margin
                        cost_line_vals = self._prepare_cost_line(
                            pol.product_id,
                            pol.product_uom_qty,
                            pol.product_uom,
                            pol.price_unit * (1 + (margin / 100)),
                            pol.name
                        )
                        order_line_vals.append((0, 0, cost_line_vals))
            self.write({"order_line": order_line_vals})

    @api.multi
    def action_shipment_plan_cancel(self):
        for order in self:
            order.trans_shipment_plan_ids.action_cancel()

    @api.multi
    def action_cancel(self):
        self.action_shipment_plan_cancel()
        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_view_shipment_plans(self):
        self.ensure_one()
        action = self.env.ref("shipment_plan.action_shipment_plan").read([])[0]
        action["domain"] = [("id", "in", self.trans_shipment_plan_ids.ids)]
        return action

    @api.multi
    def action_view_trans_prs(self):
        self.ensure_one()
        action = self.env.ref("purchase_requisition.action_purchase_requisition").read(
            []
        )[0]
        action["domain"] = [("id", "in", self.trans_pr_ids.ids)]
        return action

    @api.multi
    def action_view_trans_pos(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action").read([])[0]
        action["domain"] = [("id", "in", self.trans_po_ids.ids)]
        return action
