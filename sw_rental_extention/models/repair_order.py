# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class RepiarOrder(models.Model):
    _inherit = "repair.order"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment',
                                   domain="[('product_id','=', product_id)]")

    @api.onchange('repair_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        res = super().onchange_product_id()
        self.equipment_id = False
        return res