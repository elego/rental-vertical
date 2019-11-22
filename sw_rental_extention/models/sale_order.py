# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment',
    	                           domain="[('product_id','=', product_id)]")

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super().product_id_change()
        self.equipment_id = False
        return res