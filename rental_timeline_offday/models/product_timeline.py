# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    offday_number = fields.Float(
        "Off-Days",
        compute="_compute_fields",
        store=True,
    )

    @api.depends('res_id', 'res_model')
    def _compute_fields(self):
        super(ProductTimeline, self)._compute_fields()
        for line in self:
            if line.res_model == "sale.order.line":
                obj = self.env[line.res_model].browse(line.res_id)
                line.offday_number = obj.offday_number
