# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class RepiarOrder(models.Model):
    _inherit = "repair.order"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment')
    

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super().onchange_product_id()
        # clear old selected value
        self.equipment_id = False
        return res
