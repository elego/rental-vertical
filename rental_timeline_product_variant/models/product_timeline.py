# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    product_manu_id = fields.Many2one(
        related="product_id.manu_id",
        store=True,
    )
    product_manu_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    product_manu_type_id = fields.Many2one(
        string="Product Type of Manufacturer",
        related="product_id.manu_type_id",
        store=True,
    )

    product_manu_type_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    product_fleet_type_id = fields.Many2one(
        related="product_id.fleet_type_id",
        store=True,
    )

    product_fleet_type_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    product_license_plate = fields.Char(
        related="product_id.license_plate",
        store=True,
    )

    @api.depends('res_id', 'res_model')
    def _compute_fields(self):
        super(ProductTimeline, self)._compute_fields()
        for line in self:
            line.product_manu_name = line.product_manu_id.display_name
            line.product_manu_type_name = line.product_manu_type_id.display_name
            line.product_fleet_type_name = line.product_fleet_type_id.display_name
