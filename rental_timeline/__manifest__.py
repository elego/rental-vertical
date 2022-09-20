# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline",
    "version": "12.0.1.0.1",
    "category": "Rental",
    "summary": "Timeline view for rental orders and rental products",
    "description": """
This module provides a basic timeline view for all rental orders and the rented products.
    """,
    "usage": """
Just install this module. No further configuration is necessary.
    """,
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "depends": [
        "web_timeline",
        "rental_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/product_timeline_view.xml",
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
