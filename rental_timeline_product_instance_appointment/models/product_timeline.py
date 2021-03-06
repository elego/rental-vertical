# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    appointment = fields.Boolean(
        "Appointment",
        compute="_compute_appointment",
    )

    def _compute_appointment(self):
        for line in self:
            domain = [
                ("product_id", "=", line.product_id.id),
                ("date_next_appointment", ">=", line.date_start),
                ("date_next_appointment", "<", line.date_end),
            ]
            if bool(self.env["product.appointment"].search(domain)):
                line.appointment = True
                line.has_clues = True
