# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)

class CreateTransRequest(models.TransientModel):
    _name = "create.trans.request"
    _description = "Create Transport Purchase Request"

    origin_line_ids = fields.One2many(
        'create.trans.origin.line',
        'wizard_id',
        string='Order Lines',
    )
    service_product_ids = fields.Many2many(
        'product.product',
        string='Services',
        domain="[('is_transport', '=', True)]",
    )
    order_id = fields.Many2one(
        'sale.order',
        'Sale Order',
    )


    @api.model
    def default_get(self, fields):
        res = super(CreateTransRequest, self).default_get(fields)
        order_id = self.env.context.get('active_id', False)
        order = self.env['sale.order'].browse(order_id)
        order_lines = order.order_line.filtered(lambda l: l.trans_pr_needed)
        origin_line_ids = []
        for line in order_lines:
            origin_line_ids.append((0, 0, {
                'order_line_id': line.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
            }))
        res.update({
            'order_id': order.id,
            'origin_line_ids': origin_line_ids
        })
        return res

    def action_confirm(self):
        self.ensure_one()
        order_obj = self.env['purchase.order']
        order_line_obj = self.env['purchase.order.line']
        requisition_line_obj = self.env['purchase.requisition.line']
        uom_id = self.env.ref('uom.product_uom_unit').id
        order_lines = self.origin_line_ids.mapped('order_line_id')
        description = order_lines.get_transport_details()
        for p in self.service_product_ids:
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
                    'trans_origin_sale_line_ids': [
                        (6, 0, order_lines.ids)
                    ],
                })
                new_line.onchange_product_id()
                vals = new_line._convert_to_write(new_line._cache)
                new_line = order_line_obj.create(vals)
                new_line.name = description
            elif p.transport_service_type == 'pr':
                new_requisition = self.env['purchase.requisition'].create({
                    'name': _("Transport for %s") %(self.order_id.name),
                    'origin': self.order_id.name,
                    'description': "",
                })
                new_line = requisition_line_obj.create({
                    'requisition_id': new_requisition.id,
                    'product_id': p.id,
                    'name': description,
                    'product_qty': 1,
                    'product_uom_id': uom_id,
                    'trans_origin_sale_line_ids': [
                        (6, 0, order_lines.ids)
                    ],
                })


class CreateTransOriginLine(models.TransientModel):
    _name = "create.trans.origin.line"
    _description = "Original Sale Order Line"

    wizard_id = fields.Many2one(
        'create.trans.request',
    )
    order_line_id = fields.Many2one(
        'sale.order.line'
    )
    product_id = fields.Many2one(
        'product.product',
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
