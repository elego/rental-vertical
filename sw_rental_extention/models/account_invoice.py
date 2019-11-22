# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment',
    	                           domain="[('product_id','=', product_id)]")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        self.equipment_id = False
        return res