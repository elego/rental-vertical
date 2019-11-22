# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment',
    	                           domain="[('product_id','=', product_id)]")

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super().onchange_product_id()
        self.equipment_id = False
        return res