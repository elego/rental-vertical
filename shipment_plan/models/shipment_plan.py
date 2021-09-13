# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import logging
from odoo import fields, models, api, exceptions, _

_logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _name = "shipment.plan"
    _inherit = ["mail.thread"]
    _description = "Shipment Plan"

    name = fields.Char(
        string="Name",
        required=True,
        readonly=True,
        default="/",
        copy=False,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User",
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.uid,
    )

    initial_etd = fields.Datetime(
        string="Initial ETD",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="This is the initial estimated time of departure.",
    )

    initial_eta = fields.Datetime(
        string="Initial ETA",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="This is the  initial estimated time of arrival.",
    )

    etd = fields.Datetime(
        string="ETD",
        track_visibility="onchange",
        help="This is the up to date estimated time of departure.",
    )

    eta = fields.Datetime(
        string="ETA",
        track_visibility="onchange",
        help="This is the up to date estimated time of arrival.",
    )

    from_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="From Address",
        readonly=True,
        states={"draft": [("readonly", False)]},
        required=True,
    )

    to_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="To Address",
        readonly=True,
        states={"draft": [("readonly", False)]},
        track_visibility="onchange",
        required=True,
    )

    location_id = fields.Many2one(
        "stock.location",
        string="Source Location",
    )

    location_dest_id = fields.Many2one(
        "stock.location",
        string="Destination Location",
    )

    consignee_id = fields.Many2one(
        comodel_name="res.partner",
        string="Consignee",
        readonly=True,
        states={"draft": [("readonly", False)]},
        track_visibility="onchange",
        domain=[("is_consignee", "=", True)],
    )

    carrier_tracking_ref = fields.Char(
        string="Tracking Ref.",
        readonly=True,  # updated by wizard
        states={"draft": [("readonly", False)]},
        track_visibility="onchange",
    )

    note = fields.Text(
        string="Description / Remarks",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_transit", "In Transit"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        required=True,
        default="draft",
        copy=False,
        track_visibility="onchange",
    )

    plan_type = fields.Selection(
        string="Type",
        selection=[
            ("internal", "Internal Picking")
        ],
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    origin = fields.Char(
        string="Origin",
    )

    dangerous_goods = fields.Boolean(
        string="Dangerous Goods",
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

    trans_requisition_line_ids = fields.Many2many(
        "purchase.requisition.line",
        "rel_shipment_plan_requisition_line",
        "plan_id",
        "requisition_line_id",
        copy=False,
    )

    trans_purchase_line_ids = fields.Many2many(
        "purchase.order.line",
        "rel_shipment_plan_purchase_line",
        "plan_id",
        "purchase_line_id",
        copy=False,
    )

    trans_pr_ids = fields.One2many(
        string="Transport Requisitions",
        comodel_name="purchase.requisition",
        compute="_compute_trans_pos_prs",
    )

    trans_po_ids = fields.One2many(
        string="Transport Purchase Orders",
        comodel_name="purchase.order",
        compute="_compute_trans_pos_prs",
    )

    trans_pr_count = fields.Integer(
        compute="_compute_trans_pos_prs",
    )

    trans_po_count = fields.Integer(
        compute="_compute_trans_pos_prs",
    )

    @api.depends("move_ids")
    def _compute_picking_ids(self):
        for record in self:
            pickings = self.env["stock.picking"].browse()
            for move in record.move_ids:
                if move.picking_id:
                    pickings |= move.picking_id
            record.picking_ids = pickings
            record.picking_count = len(pickings)

    @api.multi
    @api.depends(
        "trans_purchase_line_ids",
        "trans_requisition_line_ids",
    )
    def _compute_trans_pos_prs(self):
        for order in self:
            trans_prs = self.env["purchase.requisition"]
            trans_pos = self.env["purchase.order"]
            for pr_line in order.trans_requisition_line_ids:
                trans_prs |= pr_line.requisition_id
            for po_line in order.trans_purchase_line_ids:
                trans_pos |= po_line.order_id
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
            order.trans_pr_count = len(trans_prs.ids)
            order.trans_po_count = len(trans_pos.ids)

    @api.multi
    def _get_transport_pr_name(self):
        self.ensure_one()
        return _("Transport for %s") % self.origin

    @api.model
    def _prepare_sp_po_values(self, product):
        """This function can be extended in other module"""
        self.ensure_one()
        new_order = self.env["purchase.order"].new(
            {
                "company_id": self.env.user.company_id.id,
                "partner_id": product.seller_ids[0].name.id,
            }
        )
        new_order.onchange_partner_id()
        res = new_order._convert_to_write(new_order._cache)
        return res

    @api.multi
    def _prepare_sp_pr_values(self):
        """This function can be extended in other module"""
        self.ensure_one()
        res = {
            "name": self._get_transport_pr_name(),
            "origin": self.origin,
            "schedule_date": self.initial_etd,
            "description": "",
        }

        return res

    @api.multi
    def create_purchase_request(self, service_products, transport_service_type):
        self.ensure_one()
        order_obj = self.env["purchase.order"]
        order_line_obj = self.env["purchase.order.line"]
        requisition_line_obj = self.env["purchase.requisition.line"]
        uom_id = self.env.ref("uom.product_uom_unit").id
        description = self.note
        for p in service_products:
            if transport_service_type == "po":
                if not p.seller_ids:
                    raise exceptions.UserError(
                        _("No found Supplier Info of %s") % p.name
                    )
                vals = self._prepare_sp_po_values(p)
                new_order = order_obj.create(vals)
                new_line = order_line_obj.new(
                    {
                        "order_id": new_order.id,
                        "product_id": p.id,
                        "product_qty": 1,
                        "product_uom_id": uom_id,
                    }
                )
                new_line.onchange_product_id()
                vals = new_line._convert_to_write(new_line._cache)
                if description:
                    vals["name"] = p.display_name + "\n" + description
                if self.initial_etd:
                    vals["date_planned"] = self.initial_etd
                new_line = order_line_obj.create(vals)
                self.write({"trans_purchase_line_ids": [(4, new_line.id, 0)]})
            elif transport_service_type == "pr":
                vals = self._prepare_sp_pr_values()
                new_requisition = self.env["purchase.requisition"].create(
                    vals
                )
                line_name = p.display_name
                if description:
                    line_name = p.display_name + "\n" + description
                new_line = requisition_line_obj.create(
                    {
                        "requisition_id": new_requisition.id,
                        "product_id": p.id,
                        "name": line_name,
                        "schedule_date": self.initial_etd,
                        "product_qty": 1,
                        "product_uom_id": uom_id,
                    }
                )
                self.write({"trans_requisition_line_ids": [(4, new_line.id, 0)]})

    def action_view_pickings(self):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        action["domain"] = [("id", "in", self.picking_ids.ids)]
        return action

    @api.multi
    def action_view_trans_prs(self):
        self.ensure_one()
        action = self.env.ref("purchase_requisition.action_purchase_requisition").read([])[0]
        action["domain"] = [("id", "in", self.trans_pr_ids.ids)]
        return action

    @api.multi
    def action_view_trans_pos(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action").read([])[0]
        action["domain"] = [("id", "in", self.trans_po_ids.ids)]
        return action

    @api.multi
    def action_cancel(self):
        for record in self:
            record.trans_po_ids.button_cancel()
            record.trans_pr_ids.action_cancel()
            record.state = "cancel"

    @api.multi
    def action_confirm(self):
        for record in self:
            record.state = "confirmed"

    @api.multi
    def action_done(self):
        for record in self:
            record.state = "done"

    @api.multi
    def action_cancel_draft(self):
        for record in self:
            record.state = "draft"
