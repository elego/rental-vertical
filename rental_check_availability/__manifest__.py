# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Check Availability",
    "summary": "Extends the sale_rental module for checking availability of the rented product.",
    "description": """
    Check availability of the rented product.
""",
    "usage": "",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_pricelist",
    ],
    "data": [
        "views/sale_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
