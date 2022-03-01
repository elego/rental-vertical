# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Repair",
    "summary": "extends the rental_timeline module to show the repair orders in the timeline.",
    "version": "14.0.1.0.0",
    "category": "Rental/Service",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module adds the display of repair orders related to rental products to the rental timeline view.
    """,
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_repair

No further configuration is needed.
    """,
    "depends": [
        "rental_timeline",
        "rental_repair",
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
