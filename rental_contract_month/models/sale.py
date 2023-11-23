# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.product_id and not res.display_product_id:
            res.display_product_id = res.product_id
        return res
