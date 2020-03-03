# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    # def _get_order_type(self):
    #     res = self.env['contract.order.type'].search(
    #         [('contract_type', '=', 'sale')], limit=1)
    #     return res

    type_id = fields.Many2one('contract.order.type', string="Order Type")
    sale_type_id = fields.Many2one('sale.order.type', string='Sale Order Type')

    @api.multi
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(ContractContract, self)._onchange_partner_id()
        contract_type = (self.partner_id.contract_type or
                     self.partner_id.commercial_partner_id.contract_type)
        if contract_type:
            self.type_id = contract_type
            self.contract_type = contract_type.contract_type

    @api.multi
    @api.onchange('type_id')
    def onchange_type_id(self):
        for order in self:
            if order.type_id.warehouse_id:
                order.warehouse_id = order.type_id.warehouse_id
            if order.type_id.picking_policy:
                order.picking_policy = order.type_id.picking_policy
            if order.type_id.payment_term_id:
                order.payment_term_id = order.type_id.payment_term_id.id
            if order.type_id.pricelist_id:
                order.pricelist_id = order.type_id.pricelist_id.id
            if order.type_id.incoterm_id:
                order.incoterm = order.type_id.incoterm_id.id

    @api.onchange('contract_type')
    def _onchange_contract_type(self):
        super(ContractContract, self)._onchange_contract_type()
        if self.contract_type and not self.sale_type_id:
            if self.contract_type == 'sale' :
                type_id = self.env['contract.order.type'].search(
                    [('contract_type', '=', 'sale')], limit=1)
                self.type_id = type_id.id
            if self.contract_type == 'purchase':
                type_id = self.env['contract.order.type'].search(
                    [('contract_type', '=', 'purchase')], limit=1)
                self.type_id = type_id.id

    @api.model
    def create(self, vals):
        if vals.get('type_id'):
            contract_type = self.env['contract.order.type'].browse(vals['type_id'])
            if contract_type.sequence_id:
                vals['code'] = contract_type.sequence_id.next_by_id()
        return super(ContractContract, self).create(vals)

    @api.multi
    def _prepare_invoice(self, date_invoice, journal=None):
        res = super(ContractContract, self)._prepare_invoice(date_invoice, journal)
        if self.type_id:
            res['contract_type_id'] = self.type_id.id
            if self.sale_type_id:
                # contract is created from SO
                res['sale_type_id'] = self.sale_type_id.id
            else:
                res['sale_type_id'] = False
            if self.type_id.journal_id:
                res['journal_id'] = self.type_id.journal_id.id
        return res
