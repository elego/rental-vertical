# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    shipment_plan_ids = fields.Many2many(
        "shipment.plan",
        "rel_shipment_plan_requisition_line",
        "requisition_line_id",
        "plan_id",
        copy=False,
    )

    name = fields.Char(
        string="Name",
    )

    @api.multi
    def _prepare_purchase_order_line(
        self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False
    ):
        res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(
            name=name,
            product_qty=product_qty,
            price_unit=price_unit,
            taxes_ids=taxes_ids,
        )
        if self.shipment_plan_ids:
            res["shipment_plan_ids"] = [(6, 0, self.shipment_plan_ids.ids)]
        if self.name:
            res["name"] = self.name
        if self.schedule_date:
            res["date_planned"] = fields.Datetime.to_datetime(self.schedule_date)
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    shipment_plan_ids = fields.Many2many(
        "shipment.plan",
        "rel_shipment_plan_purchase_line",
        "purchase_line_id",
        "plan_id",
        copy=False,
    )


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    selected_in_order = fields.Boolean(
        string="Selected in Order",
        help="If set, this transport request can be used "
             "as basis for a quotation/order and the transport "
             "costs can be considered charging the customer."
    )

    show_shipment_plan = fields.Boolean(
        string="Show shipment plans",
        compute="_compute_show_shipment_plan",
    )

    shipment_plan_count = fields.Integer(
        string="# Shipment Plans",
        compute="_compute_show_shipment_plan",
    )

    @api.multi
    def _compute_show_shipment_plan(self):
        for rec in self:
            rec.show_shipment_plan = False
            if any(line.shipment_plan_ids for line in rec.order_line):
                rec.show_shipment_plan = True
            rec.shipment_plan_count = len(rec.order_line.mapped('shipment_plan_ids'))

    @api.multi
    def action_transport_confirm(self):
        self.ensure_one()
        # check if the related shipment.plan has already the same confirmed service
        for line in self.order_line:
            for plan in line.shipment_plan_ids:
                for pol in plan.trans_purchase_line_ids:
                    if (
                        pol.id != line.id
                        and pol.product_id == line.product_id
                        and pol.order_id.selected_in_order
                    ):
                        raise exceptions.UserError(
                            _('You have already confirmed the "%s" in order "%s".')
                            % (pol.product_id.name, pol.order_id.name)
                        )
        self.write({"selected_in_order": True})

    @api.multi
    def action_view_shipment_plans(self):
        self.ensure_one()
        tree_view_id = self.env.ref("shipment_plan.view_shipment_plan_tree").id
        form_view_id = self.env.ref("shipment_plan.view_shipment_plan_form").id
        return {
            "type": "ir.actions.act_window",
            "name": _("Shipment Plans"),
            "target": "current",
            "view_mode": "tree,form",
            "view_ids": [tree_view_id, form_view_id],
            "res_model": "shipment.plan",
            "domain": "[('id','in',["
            + ",".join(map(str, self.order_line.mapped("shipment_plan_ids").mapped("id")))
            + "])]",
        }
