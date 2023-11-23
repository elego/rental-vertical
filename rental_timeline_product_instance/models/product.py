# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    instance_state = fields.Selection(
        compute="_compute_instance_state", search="_search_instance_state"
    )

    def _compute_instance_state(self):
        super()._compute_instance_state()
        timeline_obj = self.env["product.timeline"]
        today = fields.Date.today()
        for product in self:
            timelines = timeline_obj.search(
                [
                    ("product_id", "=", product.id),
                    ("date_start", "<=", today),
                    ("date_end", ">=", today),
                ]
            )
            if timelines:
                if any(line.type == "rental" for line in timelines):
                    product.instance_state = "rental"
                elif any(line.type == "reserved" for line in timelines):
                    product.instance_state = "reserved"

    def _search_instance_state(self, operator, value):
        if operator in ["="] and value in ["available", "reserved", "rental"]:
            all_products = self.env["product.product"].search([])
            if value == "available":
                available_products = all_products.filtered(
                    lambda p: p.instance_state == "available"
                )
                return [("id", "in", available_products.ids)]
            elif value == "reserved":
                reserved_products = all_products.filtered(
                    lambda p: p.instance_state == "reserved"
                )
                return [("id", "in", reserved_products.ids)]
            elif value == "rental":
                rental_products = all_products.filtered(
                    lambda p: p.instance_state == "rental"
                )
                return [("id", "in", rental_products.ids)]
            else:
                return expression.FALSE_DOMAIN

        return super()._search_instance_state(operator, value)
