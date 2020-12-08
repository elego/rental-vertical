# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dangerous_goods = fields.Boolean(
        "Dangerous Goods"
    )

    trans_pr_needed = fields.Boolean(
        "Transport PR Needed",
        compute="_compute_trans_pr_needed"
    )
    trans_shipment_plan_id = fields.Many2one(
        'shipment.plan',
        "Shipment Plan",
        ondelete="set null",
        copy=False,
    )
    trans_requisition_line_ids = fields.Many2many(
        'purchase.requisition.line',
        related="trans_shipment_plan_id.trans_requisition_line_ids",
        string="Transfer Requisition Line",
    )
    trans_purchase_line_ids = fields.Many2many(
        'purchase.order.line',
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

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id=group_id)
        import wdb; wdb.set_trace()
        if self.trans_shipment_plan_id:
            res['shipment_plan_id'] = self.trans_shipment_plan_id.id
        return res

    def _get_custom_move_fields(self):
        res = super()._get_custom_move_fields()
        import wdb; wdb.set_trace()
        res.append('shipment_plan_id')
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
    transport_cost_type = fields.Selection(
        [('single', 'Single Position'), ('multi', 'Multi Positions')],
        default=_default_transport_cost_type,
    )
    trans_shipment_plan_ids = fields.Many2many(
        'shipment.plan',
        compute="_compute_shipment_plans",
    )
    trans_pr_ids = fields.One2many(
        'purchase.requisition',
        compute="_compute_shipment_plans",
    )
    trans_po_ids = fields.One2many(
        'purchase.order',
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
        'order_line',
        'order_line.trans_shipment_plan_id',
        'order_line.trans_shipment_plan_id.trans_purchase_line_ids',
        'order_line.trans_shipment_plan_id.trans_requisition_line_ids',
    )
    def _compute_shipment_plans(self):
        for order in self:
            trans_sps = self.env['shipment.plan'].browse()
            trans_prs = self.env['purchase.requisition'].browse()
            trans_pos = self.env['purchase.order'].browse()
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

    @api.multi
    def action_create_trans_cost(self):
        self.ensure_one()
        price_unit = sum([p.amount_untaxed \
            for p in self.trans_po_ids if p.selected_in_order])
        margin = 0
        if price_unit == 0:
            raise exceptions.UserError(
                _('You need to select a transport purchase RFQ for this sale order first'))
        if self.transport_cost_type == "single":
            cost = 0
            name = ''
            for p in self.trans_po_ids:
                if p.selected_in_order:
                    for pol in p.order_line:
                        margin = pol.product_id.transport_sales_margin
                        cost += pol.price_unit * (1 + (margin/100))
                        name += '%s\n' %pol.product_id.name
            product_id = self.env['ir.config_parameter'].sudo().get_param(
                'sale.transport_cost_product_id')
            product_transport_cost = self.env['product.product'].browse(
                int(product_id))
            self.write({'order_line': [(0, 0, {
                'product_id': product_transport_cost.id,
                'product_uom_qty': 1,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'price_unit': cost,
                'name': name,
            })]})
        elif self.transport_cost_type == "multi":
            order_line_vals = []
            for p in self.trans_po_ids:
                if p.selected_in_order:
                    for pol in p.order_line:
                        margin = pol.product_id.transport_sales_margin
                        order_line_vals.append((0, 0, {
                            'product_id': pol.product_id.id,
                            'product_uom_qty': pol.product_uom_qty,
                            'product_uom': pol.product_uom.id,
                            'price_unit': pol.price_unit * (1 + (margin/100)),
                            'name': pol.name,
                        }))
            self.write({'order_line': order_line_vals})

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
        action = self.env.ref(
            'shipment_plan.action_shipment_plan'
        ).read([])[0]
        action['domain'] = [('id','in', self.trans_shipment_plan_ids.ids)]
        return action

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
