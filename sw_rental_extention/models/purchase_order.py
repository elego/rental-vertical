# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment')

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super().onchange_product_id()
        # clear old selected value
        self.equipment_id = False
        return res

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        # set domain on Analytic Account
        # clear old selected value
        self.account_analytic_id = False
        if self.equipment_id:
            domain = { 'account_analytic_id': [ ('id', '=', self.equipment_id.analytic_account_id.id) ] } 
            return { 'domain': domain }

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        # set equipment_id from purchase.orde.line to stock.move
        if self.equipment_id:
            vals_dic = res[0]
            vals_dic.update({'equipment_id': self.equipment_id.id})
        return res