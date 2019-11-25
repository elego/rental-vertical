# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super().product_id_change()
        # clear old selected value
        self.equipment_id = False
        return res

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        # update field from sale.orde.line to stock.move
        res.update({'equipment_id': self.equipment_id.id})
        return res

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                           name, origin, values, group_id)
        # update field from sale.orde.line to stock.move
        res['equipment_id'] = values.get('equipment_id', False)
        return res
