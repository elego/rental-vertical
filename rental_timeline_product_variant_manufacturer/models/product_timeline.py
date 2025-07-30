# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    product_manu_id = fields.Many2one(
        related="product_id.manu_id",
        store=True,
    )
    product_manu_name = fields.Char(
        compute="_compute_variant_fields",
        store=True,
    )

    product_manu_type_id = fields.Many2one(
        string="Product Type of Manufacturer",
        related="product_id.manu_type_id",
        store=True,
    )

    product_manu_type_name = fields.Char(
        compute="_compute_variant_fields",
        store=True,
    )

    @api.depends(
        "product_id",
        "product_manu_id",
        "product_manu_id.name",
        "product_manu_type_id",
        "product_manu_type_id.name",
    )
    def _compute_variant_fields(self):
        for line in self:
            line.product_manu_name = line.product_manu_id.display_name
            line.product_manu_type_name = line.product_manu_type_id.display_name
