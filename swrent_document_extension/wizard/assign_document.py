# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _


class AssignDocument(models.TransientModel):
    _name = 'assign.document'
    _description = 'Assign Documents to Record'

    res_model = fields.Selection(string="Model",
        selection=[
            ('product.product','Product'),
            ('sale.order','Sale Order'),
            ('purchase.order','Purchase Order'),
            ('stock.picking','Shipment'),
            ('account.invoice','Invoice'),
        ])
    res_id = fields.Integer('Res ID', compute="_compute_res_id")
    product_id = fields.Many2one('product.product', 'Product')
    invoice_id = fields.Many2one('account.invoice', 'Invoice')
    picking_id = fields.Many2one('stock.picking', 'Shipment')
    sale_id = fields.Many2one('sale.order', 'Sale Order')
    purchase_id = fields.Many2one('purchase.order', 'Purchase Order')

    @api.multi
    @api.depends('res_model', 'product_id', 'invoice_id', 'picking_id', 'sale_id', 'purchase_id')
    def _compute_res_id(self):
        for doc in self:
            doc.res_id = False
            if doc.res_model == 'product.product':
                doc.res_id = doc.product_id and doc.product_id.id or False
            elif doc.res_model == 'account.invoice':
                doc.res_id = doc.invoice_id and doc.invoice_id.id or False
            elif doc.res_model == 'stock.picking':
                doc.res_id = doc.picking_id and doc.picking_id.id or False
            elif doc.res_model == 'sale.order':
                doc.res_id = doc.sale_id and doc.sale_id.id or False
            elif doc.res_model == 'purchase.order':
                doc.res_id = doc.purchase_id and doc.purchase_id.id or False

    @api.model
    def default_get(self, fields):
        res = {}
        model = self._context.get('active_model', False)
        active_id = self._context.get('active_ids', []) and self._context.get('active_ids', [])[0] or self._context.get('active_id', False)
        if active_id:
            doc = self.env[model].browse(active_id)
            res['res_model'] = doc.res_model
        return res

    @api.multi
    def action_done(self):
        self.ensure_one()
        model = self._context.get('active_model', False)
        active_ids = self._context.get('active_ids', [])
        if not active_ids:
            action_ids = self._context.get('active_id', False) and [self._context.get('active_id')] or []
        docs = self.env[model].browse(active_ids)
        docs.action_assign(self.res_model, self.res_id)
        return {'type': 'ir.actions.act_window_close'}
