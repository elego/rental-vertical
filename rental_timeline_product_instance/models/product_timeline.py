# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    product_instance_next_service_date = fields.Date(
        related="product_id.instance_next_service_date",
        store=True,
    )

    product_instance_current_location_id = fields.Many2one(
        related="product_id.instance_current_location_id",
        store=True,
    )

    product_instance_current_location_name = fields.Char(
        compute="_compute_instance_fields",
        store=True,
    )

    product_instance_serial_number_id = fields.Many2one(
        related="product_id.instance_serial_number_id",
        store=True,
    )

    product_instance_serial_number_name = fields.Char(
        compute="_compute_instance_fields",
        store=True,
    )

    @api.depends(
        "product_instance_serial_number_id",
        "product_instance_current_location_id",
    )
    def _compute_instance_fields(self):
        for line in self:
            line.product_instance_serial_number_name = (
                line.product_instance_serial_number_id.display_name
            )
            line.product_instance_current_location_name = (
                line.product_instance_current_location_id.display_name
            )

    @api.multi
    @api.constrains("date_start", "date_end", "type")
    def _check_date(self):
        for line in self:
            if line.type == "rental":
                domain = [
                    ("date_start", "<", line.date_end),
                    ("date_end", ">", line.date_start),
                    ("product_id", "=", line.product_id.id),
                    ("product_id.product_instance", "=", True),
                    ("type", "=", "rental"),
                    ("id", "!=", line.id),
                ]
                lines = self.search_count(domain)
                if lines:
                    msg = _(
                        "You can not have 2 timelines that overlaps on the same day."
                    )
                    raise exceptions.ValidationError(msg)
