# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import logging
from odoo import fields, models, api, exceptions, _

_logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _name = "shipment.plan"
    _inherit = ['mail.thread']

    _description = "Shipment Plan"

    name = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default='/',
        copy=False,
    )
    user_id = fields.Many2one(
        'res.users', 'Responsible',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.uid,
    )
    initial_etd = fields.Datetime(
        'Initial ETD',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Initial Estimated Time of Departure"
    )
    initial_eta = fields.Datetime(
        'Initial ETA',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Initial Estimated Time of Arrival"
    )
    etd = fields.Datetime(
        'ETD',
        track_visibility='onchange',
        help="Up to date Estimated Time of Departure"
    )
    eta = fields.Datetime(
        'ETA',
        track_visibility='onchange',
        help="Up to date Estimated Time of Arrival"
    )
    from_address_id = fields.Many2one(
        'res.partner', 'From Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        required=True,
    )
    to_address_id = fields.Many2one(
        'res.partner',
        'To Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
        required=True,
    )
    consignee_id = fields.Many2one(
        'res.partner',
        'Consignee',
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
        domain=[('is_consignee', '=', True)],
    )
    carrier_tracking_ref = fields.Char(
        'Tracking Ref.',
        readonly=True,  # updated by wizard
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    note = fields.Text(
        'Description / Remarks',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('in_transit', 'In Transit'),
         ('done', 'Done'),
         ('cancel', 'Cancel')
         ],
        required=True,
        default='draft',
        copy=False,
        track_visibility='onchange',
    )
    plan_type = fields.Selection(
        string="Type",
        selection=[
        ],
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    origin = fields.Char('Origin Ref')
    dangerous_goods = fields.Boolean(
        "Dangerous Goods"
    )
    trans_requisition_line_ids = fields.Many2many(
        'purchase.requisition.line',
        'rel_shipment_plan_requisition_line',
        'plan_id',
        'requisition_line_id',
        copy=False,
    )
    trans_purchase_line_ids = fields.Many2many(
        'purchase.order.line',
        'rel_shipment_plan_purchase_line',
        'plan_id',
        'purchase_line_id',
        copy=False,
    )
    trans_pr_ids = fields.One2many(
        'purchase.requisition',
        compute="_compute_trans_pos_prs",
    )
    trans_po_ids = fields.One2many(
        'purchase.order',
        compute="_compute_trans_pos_prs",
    )
    trans_pr_count = fields.Integer(
        compute="_compute_trans_pos_prs"
    )
    trans_po_count = fields.Integer(
        compute="_compute_trans_pos_prs"
    )

    @api.multi
    def _compute_trans_pos_prs(self):
        for order in self:
            trans_prs = self.env['purchase.requisition'].browse()
            trans_pos = self.env['purchase.order'].browse()
            for pr_line in order.trans_requisition_line_ids:
                trans_prs |= pr_line.requisition_id
            for po_line in order.trans_purchase_line_ids:
                trans_pos |= po_line.order_id
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
            order.trans_pr_count = len(trans_prs.ids)
            order.trans_po_count = len(trans_pos.ids)

    @api.multi
    def create_purchase_request(self, service_products):
        self.ensure_one()
        order_obj = self.env['purchase.order']
        order_line_obj = self.env['purchase.order.line']
        requisition_line_obj = self.env['purchase.requisition.line']
        uom_id = self.env.ref('uom.product_uom_unit').id
        description = self.note
        for p in service_products:
            if p.transport_service_type == 'po':
                if not p.seller_ids:
                    raise exceptions.UserError(
                        _('No found Supplier Info of %s') %p.name
                    )
                new_order = order_obj.new({
                    'company_id': self.env.user.company_id.id,
                    'partner_id': p.seller_ids[0].name.id,
                })
                new_order.onchange_partner_id()
                vals = new_order._convert_to_write(new_order._cache)
                new_order = order_obj.create(vals)
                new_line = order_line_obj.new({
                    'order_id': new_order.id,
                    'product_id': p.id,
                    'product_qty': 1,
                    'product_uom_id': uom_id,
                })
                new_line.onchange_product_id()
                vals = new_line._convert_to_write(new_line._cache)
                if description:
                    vals['name'] = description
                if self.initial_etd:
                    vals['date_planned'] = self.initial_etd
                new_line = order_line_obj.create(vals)
                self.write({
                    'trans_purchase_line_ids': [(4, new_line.id, 0)]
                })
            elif p.transport_service_type == 'pr':
                new_requisition = self.env['purchase.requisition'].create({
                    'name': _("Transport for %s") %(self.origin),
                    'origin': self.origin,
                    'schedule_date': self.initial_etd,
                    'description': "",
                })
                new_line = requisition_line_obj.create({
                    'requisition_id': new_requisition.id,
                    'product_id': p.id,
                    'name': description,
                    'schedule_date': self.initial_etd,
                    'product_qty': 1,
                    'product_uom_id': uom_id,
                })
                self.write({
                    'trans_requisition_line_ids': [(4, new_line.id, 0)]
                })

    @api.multi
    def action_view_trans_prs(self):
        self.ensure_one()
        action = self.env.ref(
            'purchase_requisition.action_purchase_requisition'
        ).read([])[0]
        action['domain'] = [('id','in', self.trans_pr_ids.ids)]
        return action

    @api.multi
    def action_view_trans_pos(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_form_action').read([])[0]
        action['domain'] = [('id','in', self.trans_po_ids.ids)]
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
