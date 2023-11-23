# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_insurance = fields.Boolean(
        string="Insurance",
        default=False,
        help="This product is a insurance.",
    )
