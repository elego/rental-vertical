# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, exceptions, _


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.multi
    @api.constrains('product_id', 'name')
    def _check_unique_product_instance(self):
        for rec in self:
            if rec.product_id.product_instance:
                domain = [
                    ('product_id', '=', rec.product_id.id),
                    ('id', '!=', rec.id),
                ]
                res = self.search_count(domain)
                if res:
                    raise exceptions.ValidationError(
                        _('You can not have 2 serial numbers for a product instance.'))

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if vals.get('state', False) == 'done':
            for m in self:
                if m.product_id.product_instance:
                    m.product_id.current_location_id = m.location_dest_id