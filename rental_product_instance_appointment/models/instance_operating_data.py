# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class InstanceOperatingData(models.Model):
    _inherit = 'instance.operating.data'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.instance_id.update_operating_data_daily_increase()
        return res

    @api.multi
    def write(self, values):
        res = super().write(values)
        self.mapped('instance_id').update_operating_data_daily_increase()
        return res
