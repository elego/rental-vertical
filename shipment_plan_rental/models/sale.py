# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    trans_return_shipment_plan_id = fields.Many2one(
        "shipment.plan",
        "Shipment Plan (Return)",
        ondelete="set null",
        copy=False,
    )
    trans_return_requisition_line_ids = fields.Many2many(
        "purchase.requisition.line",
        related="trans_return_shipment_plan_id.trans_requisition_line_ids",
        string="Transfer Requisition Line (Return)",
    )
    trans_return_purchase_line_ids = fields.Many2many(
        "purchase.order.line",
        related="trans_return_shipment_plan_id.trans_purchase_line_ids",
        string="Transfer Purchase Line (Return)",
    )

    # (override)
    @api.multi
    def get_transport_details(self):
        order = self[0].order_id
        res = ""
        src_address = self.env.user.company_id.partner_id._display_address(
            without_company=True
        )
        dest_address = order.partner_shipping_id._display_address(
            without_company=True
        )
        res += "Incoterm: %s \n" % (order.incoterm.name)
        for line in self:
            product_name = line.product_id.name
            if line.product_id.rented_product_id:
                product_name = line.product_id.rented_product_id.name
            res += "%s: %s %s \n" % (
                product_name,
                line.product_uom_qty,
                line.product_id.uom_id.name,
            )
        if self.env.context.get("shipment_plan_return", False):
            res += "Date: %s \n" % (order.default_end_date)
            res += "Source Address: \n %s \n\n" % (dest_address)
            res += "Destination Address:\n %s \n\n" % (src_address)
        else:
            res += "Date: %s \n" % (order.default_start_date)
            res += "Source Address: \n %s \n\n" % (src_address)
            res += "Destination Address: \n %s \n\n" % (dest_address)
        return res

    def _prepare_new_rental_procurement_values(self, group=False):
        res = super()._prepare_new_rental_procurement_values(group=group)
        if self.trans_shipment_plan_id:
            res["shipment_plan_id"] = self.trans_shipment_plan_id.id
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # (override)
    @api.multi
    def _compute_shipment_plans(self):
        for order in self:
            trans_sps = self.env["shipment.plan"].browse()
            trans_prs = self.env["purchase.requisition"].browse()
            trans_pos = self.env["purchase.order"].browse()
            for line in order.order_line:
                if line.trans_shipment_plan_id:
                    trans_sps |= line.trans_shipment_plan_id
                if line.trans_return_shipment_plan_id:
                    trans_sps |= line.trans_return_shipment_plan_id
                for pr_line in line.trans_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_purchase_line_ids:
                    trans_pos |= po_line.order_id
                for pr_line in line.trans_return_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_return_purchase_line_ids:
                    trans_pos |= po_line.order_id
            order.trans_shipment_plan_ids = trans_sps
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
            order.trans_shipment_plan_count = len(trans_sps.ids)
            order.trans_pr_count = len(trans_prs.ids)
            order.trans_po_count = len(trans_pos.ids)
