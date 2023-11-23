# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    @api.onchange("product_id")
    def onchange_product_id(self):
        super(RepairOrder, self).onchange_product_id()
        if self.product_id and self.product_id.instance_serial_number_id:
            self.lot_id = self.product_id.instance_serial_number_id.id
