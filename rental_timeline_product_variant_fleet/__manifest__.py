# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Product Variant Fleet",
    "summary": "Extends the rental_timeline_product_variant_manufacturer module to add fields.",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
Extends the rental_timeline_product_variant_manufacturer module to add fields..
    """,
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_product_variant_fleet
- rental_timeline_product_variant_manufacturer

No further configuration is needed.
    """,
    "depends": [
        "rental_product_variant_fleet",
        "rental_timeline_product_variant_manufacturer",
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
