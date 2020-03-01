# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    planned_source_address_id = fields.Many2one('res.partner', string="Planned Source Address")
    trans_pr_needed = fields.Boolean(
        "Transport PR Needed",
        compute="_compute_trans_pr_needed")
    trans_pr_created = fields.Boolean(
        "Transport PR Created",
        compute="_compute_trans_pr_created")
    trans_purchase_id = fields.Many2one('purchase.order', compute="_compute_trans_purchase_id")

    def _compute_trans_purchase_id(self):
        pol_obj = self.env['purchase.order.line']
        for line in self:
            pol_lines = pol_obj.search([
                ('trans_origin_sale_line_id', '=', line.id),
                ('state', '!=', 'cancel'),
            ])
            line.trans_purchase_id = pol_lines and pol_lines[0].order_id or False

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
    def _compute_trans_pr_created(self):
        for line in self:
            line.trans_pr_created = False
            if line.trans_pr_needed:
                if line.trans_purchase_id and line.trans_purchase_id.state in ['purchase', 'done']:
                    line.trans_pr_created = True

    def _get_trans_pr_details(self):
        res = ""
        if self.trans_pr_needed:
            src_address = self.env.user.company_id.with_context(
                show_address=True).display_name
            if self.planned_source_address_id:
                source_address = self.planned_source_address_id.with_context(
                    show_address=True).display_name
            dest_address = self.order_id.partner_shipping_id.with_context(
                show_address=True).display_name
            res += "Incoterm: %s \n" %(self.order_id.incoterm.name)
            res += "%s: %s %s \n" %(
                self.product_id.name, self.rental_qty, self.product_id.uom_id.name)
            res += "Date of Arrival: %s \n" %(self.start_date)
            res += "Source Address: %s \n" %(src_address)
            res += "Destination Address: %s \n" %(dest_address)
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trans_pr_needed = fields.Boolean(
        "Transport PR Needed",
        compute="_compute_trans_pr_needed")
    trans_pr_created = fields.Boolean(
        "Transport PR Created",
        compute="_compute_trans_pr_created")
    trans_cost_created = fields.Boolean(
        "Transport Cost Created", copy=False)
    trans_pr_ids = fields.One2many('purchase.requisition', compute="_compute_trans_pos_prs")
    trans_po_ids = fields.One2many('purchase.order', compute="_compute_trans_pos_prs")
    trans_pr_count = fields.Integer(compute="_compute_trans_pos_prs")
    trans_po_count = fields.Integer(compute="_compute_trans_pos_prs")

    @api.multi
    def _compute_trans_pos_prs(self):
        for order in self:
            trans_prs = self.env['purchase.requisition'].browse()
            trans_pos = self.env['purchase.order'].browse()
            for line in order.order_line:
                trans_pr_lines = self.env['purchase.requisition.line'].search([
                    ('trans_origin_sale_line_id', '=', line.id)])
                for pr_line in trans_pr_lines:
                    trans_prs |= pr_line.requisition_id
                trans_po_lines = self.env['purchase.order.line'].search([
                    ('trans_origin_sale_line_id', '=', line.id)])
                for po_line in trans_po_lines:
                    trans_pos |= po_line.order_id
            self.trans_pr_ids = trans_prs
            self.trans_po_ids = trans_pos
            self.trans_pr_count = len(trans_prs.ids)
            self.trans_po_count = len(trans_pos.ids)

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

    @api.multi
    def _compute_trans_pr_created(self):
        for order in self:
            order.trans_pr_created = False
            trans_pr_needed_lines = order.order_line.filtered(lambda l: l.trans_pr_needed)
            order.trans_pr_created = all(l.trans_pr_created for l in trans_pr_needed_lines)

    @api.multi
    def action_create_trans_pr(self):
        product_transport = self.env.ref('rental_transport_purchase_request.product_transport')
        res = {}
        for order in self:
            line_vals = []
            if order.trans_pr_needed:
                for line in order.order_line:
                    line_vals.append((0, 0, {
                        'name': line._get_trans_pr_details(),
                        'product_id': product_transport.id,
                        'product_qty': 1,
                        'product_uom_id': self.env.ref('uom.product_uom_unit').id,
                        'trans_origin_sale_line_id': line.id,
                        'schedule_date': line.start_date - timedelta(days=line.customer_lead),
                    }))
                requisition = self.env['purchase.requisition'].create({
                    'name': _("Transport for %s") %(order.name),
                    'origin': order.name,
                    'description': "",
                    'line_ids': line_vals,
                })
                res[order.id] = requisition
        return res

    @api.multi
    def action_create_trans_cost(self):
        self.ensure_one()
        product_transport = self.env.ref('rental_transport_purchase_request.product_transport')
        trans_pr_needed_lines = self.order_line.filtered(lambda l: l.trans_pr_needed)
        if self.trans_pr_created:
            purchase_orders = self.env['purchase.order']
            for line in trans_pr_needed_lines:
                purchase_orders |= line.trans_purchase_id
            price_unit = sum([p.amount_untaxed for p in purchase_orders])
            self.write({'order_line': [(0, 0, {
                'product_id': product_transport.id,
                'product_uom_qty': 1,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'price_unit': price_unit,
            })]})
            self.trans_cost_created = True
        else:
            for line in trans_pr_needed_lines:
                if not line.trans_pr_created:
                    raise exceptions.UserError(
                        _('You have to buy the transport service for %s') %line.product_id.name)

    @api.multi
    def action_cancel_trans_order(self):
        for order in self:
            for line in order.order_line:
                trans_purchase = line.trans_purchase_id
                if line.trans_pr_needed and trans_purchase:
                    if trans_purchase.state == 'draft':
                        trans_purchase.button_cancel()
                    elif trans_purchase.state == 'cancel':
                        continue
                    else:
                        raise exceptions.UserError(
                            _('You have to cancel the transport server "%s" at first.') %trans_purchase.name)

    @api.multi
    def action_cancel_trans_requisition(self):
        for order in self:
            order.trans_pr_ids.action_cancel()

    @api.multi
    def action_cancel(self):
        self.action_cancel_trans_order()
        self.action_cancel_trans_requisition()
        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_view_trans_prs(self):
        self.ensure_one()
        action = self.env.ref('purchase_requisition.action_purchase_requisition').read([])[0]
        action['domain'] = [('id','in', self.trans_pr_ids.ids)]
        return action

    @api.multi
    def action_view_trans_pos(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_form_action').read([])[0]
        action['domain'] = [('id','in', self.trans_po_ids.ids)]
        return action
