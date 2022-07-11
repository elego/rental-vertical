# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    manu_year = fields.Char(
        string="Year of Manufacture",
    )
    manu_id = fields.Many2one(
        comodel_name="product.manufacturer",
        string="Manufacturer",
    )
    manu_type_id = fields.Many2one(
        comodel_name="product.manufacturer.type",
        string="Type",
        ondelete="set null",
    )

class ProductManufacturer(models.Model):
    _name = "product.manufacturer"
    _description = "Product Manufacturer"

    name = fields.Char(
        string="Name",
    )
    manufacturer_type_ids = fields.One2many(
        comodel_name="product.manufacturer.type",
        inverse_name="manufacturer_id",
    )

# ---need to remove below class
class ProductManufacturerType(models.Model):
    _name = "product.manufacturer.type"
    _description = "Product Manufacturer Type"

    name = fields.Char(
        string="Name",
    )
    manufacturer_id = fields.Many2one(
        comodel_name="product.manufacturer",
        string="Manufacturer",
    )
