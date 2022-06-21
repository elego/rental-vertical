# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Variant Manufacturer",
    "summary": "Extends model product with manufacturer fields for rental use cases.",
    "description": """
This module adds several fields to the product form.

Additional fields:
 - manu_year [Char]: year of manufacture
 - manu_id [Many2one]: product.manufacturer -- manufacturer
 - manu_type_id [Many2one]: product.manufacturer.type -- type
""",
    "usage": """
In order to get manufacturer related fields, open the product form view.
""",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_product_variant",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "auto_install": True,
    "license": "AGPL-3",
}
