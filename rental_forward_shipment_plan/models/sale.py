# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # (override)
    @api.multi
    def _compute_shipment_plans(self):
        for order in self:
            trans_sps = self.env["shipment.plan"]
            forward_trans_sps = self.env["shipment.plan"]
            trans_prs = self.env["purchase.requisition"]
            trans_pos = self.env["purchase.order"]
            for line in order.order_line:
                if line.trans_shipment_plan_id:
                    trans_sps |= line.trans_shipment_plan_id
                    # add forward shipment_plan
                    forward_trans_sps |= (
                        line.trans_shipment_plan_id.forward_shipment_plan_ids
                    )
                if line.trans_return_shipment_plan_id:
                    trans_sps |= line.trans_return_shipment_plan_id
                    # add forward shipment_plan
                    forward_trans_sps |= (
                        line.trans_return_shipment_plan_id.forward_shipment_plan_ids
                    )
                for pr_line in line.trans_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_purchase_line_ids:
                    trans_pos |= po_line.order_id
                for pr_line in line.trans_return_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_return_purchase_line_ids:
                    trans_pos |= po_line.order_id
            # add prs and pos of forward shipment_plan
            for forward_sp in forward_trans_sps:
                for prl in forward_sp.trans_requisition_line_ids:
                    trans_prs |= prl.requisition_id
                for pol in forward_sp.trans_purchase_line_ids:
                    trans_pos |= pol.order_id
            trans_sps |= forward_trans_sps
            order.trans_shipment_plan_ids = trans_sps
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
            order.trans_shipment_plan_count = len(trans_sps.ids)
            order.trans_pr_count = len(trans_prs.ids)
            order.trans_po_count = len(trans_pos.ids)
