# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    product_fleet_type_id = fields.Many2one(
        related="product_id.fleet_type_id",
        store=True,
    )

    product_fleet_type_name = fields.Char(
        compute="_compute_variant_fields",
        store=True,
    )

    product_license_plate = fields.Char(
        related="product_id.license_plate",
        store=True,
    )

    @api.depends(
        "product_id",
        "product_id.license_plate",
        "product_manu_id",
        "product_manu_id.name",
        "product_manu_type_id",
        "product_manu_type_id.name",
        "product_fleet_type_id",
        "product_fleet_type_id.name",
    )
    def _compute_variant_fields(self):
        res = super(ProductTimeline, self)._compute_variant_fields()
        for line in self:
            line.product_fleet_type_name = line.product_fleet_type_id.display_name
        return res
