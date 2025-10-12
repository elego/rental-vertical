# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    appointment = fields.Boolean(
        "Appointment",
        compute="_compute_appointment",
    )

    def _compute_appointment(self):
        Appointment = self.env["product.appointment"]
        for line in self:
            line.appointment = False
            line.has_clues = False

            if line.date_start and line.date_end and line.product_id: 
                domain = [
                    ("product_id", "=", line.product_id.id),
                    ("date_next_appointment", ">=", line.date_start),
                    ("date_next_appointment", "<", line.date_end),
                ]
            if bool(Appointment.search(domain)):
                line.appointment = True
                line.has_clues = True
