# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Product Instance Maintenance",
    "summary": "Extends the rental_timeline_product_instance module to add fields.",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
Extends the rental_timeline_product_instance module to add fields..
    """,
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline_product_instance

No further configuration is needed.
    """,
    "depends": [
        "rental_timeline_product_instance",
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
