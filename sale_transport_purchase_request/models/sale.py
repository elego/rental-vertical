# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trans_pr_needed = fields.Boolean(
        "Transport PR Needed",
        compute="_compute_trans_pr_needed"
    )
    trans_requisition_line_ids = fields.Many2many(
        'purchase.requisition.line',
        'rel_trans_sale_requisition_line',
        'sale_line_id',
        'requisition_line_id',
        copy=False,
    )
    trans_purchase_line_ids = fields.Many2many(
        'purchase.order.line',
        'rel_trans_sale_purchase_line',
        'sale_line_id',
        'purchase_line_id',
        copy=False,
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
        src_address = self.env.user.company_id.with_context(
            show_address=True).display_name
        dest_address = order.partner_shipping_id.with_context(
            show_address=True).display_name
        res += "Incoterm: %s \n" %(order.incoterm.name)
        for line in self:
            res += "%s: %s %s \n" %(
                line.product_id.name,
                line.product_uom_qty,
                line.product_id.uom_id.name
            )
        res += "Date: %s \n" %(order.date_order)
        res += "Source Address: %s \n" %(src_address)
        res += "Destination Address: %s \n" %(dest_address)
        return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_transport_cost_type(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'sale.sale_transport_cost_type')

    trans_pr_needed = fields.Boolean(
        "Transport PR Needed",
        compute="_compute_trans_pr_needed",
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
    transport_cost_type = fields.Selection(
        [('single', 'Single Position'), ('multi', 'Multi Positions')],
        default=_default_transport_cost_type,
    )

    @api.multi
    def _compute_trans_pos_prs(self):
        for order in self:
            trans_prs = self.env['purchase.requisition'].browse()
            trans_pos = self.env['purchase.order'].browse()
            for line in order.order_line:
                for pr_line in line.trans_requisition_line_ids:
                    trans_prs |= pr_line.requisition_id
                for po_line in line.trans_purchase_line_ids:
                    trans_pos |= po_line.order_id
            order.trans_pr_ids = trans_prs
            order.trans_po_ids = trans_pos
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

    @api.multi
    def action_create_trans_cost(self):
        self.ensure_one()
        price_unit = sum([p.amount_untaxed \
            for p in self.trans_po_ids if p.transport_confirmed])
        if price_unit == 0:
            return
        if self.transport_cost_type == "single":
            product_id = self.env['ir.config_parameter'].sudo().get_param(
                'sale.transport_cost_product_id')
            product_transport_cost = self.env['product.product'].browse(
                int(product_id))
            self.write({'order_line': [(0, 0, {
                'product_id': product_transport_cost.id,
                'product_uom_qty': 1,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'price_unit': price_unit,
            })]})
        elif self.transport_cost_type == "multi":
            order_line_vals = []
            for p in self.trans_po_ids:
                if p.transport_confirmed:
                    for pol in p.order_line:
                        order_line_vals.append((0, 0, {
                            'product_id': pol.product_id.id,
                            'product_uom_qty': pol.product_uom_qty,
                            'product_uom': pol.product_uom.id,
                            'price_unit': pol.price_unit,
                            'name': pol.name,
                        }))
            self.write({'order_line': order_line_vals})

    @api.multi
    def action_cancel_trans_order(self):
        for order in self:
            order.trans_po_ids.action_cancel()

    @api.multi
    def action_cancel_trans_requisition(self):
        for order in self:
            order.trans_pr_ids.action_cancel()

    @api.multi
    def button_cancel(self):
        self.action_cancel_trans_order()
        self.action_cancel_trans_requisition()
        return super(SaleOrder, self).action_cancel()

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
