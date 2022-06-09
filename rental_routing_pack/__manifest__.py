# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Routing Pack",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "summary": "Rental Routing Pack",
    "description": """
This module allows to routing rentals with product packs.
You can plan you rentals to bypass the product in pack (without pack) between customers.
""",
    "usage": """
Install the module.
No further configuration is needed.
""",

    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "depends": [
        "rental_product_pack",
        "rental_routing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/rental_pack_product_route_view.xml",
        "views/sale_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
