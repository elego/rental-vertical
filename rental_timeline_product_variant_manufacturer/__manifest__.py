# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Product Variant Manufacturer",
    "summary": "Extends the rental_timeline module to show the product variant fields in the timeline product popup.",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module adds the display of product variant-specific fields to the rental timeline view.
    """,
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_product_variant

No further configuration is needed.
    """,
    "depends": [
        "rental_timeline",
        "rental_product_variant",
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
