# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Pack",
    "version": "16.0.1.0.0",
    "category": "Rental",
    "summary": "Manage rentals with product packs",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
This module allows to manage rentals with product packs.
You can define product packs as described in the module product_pack.
The components of the pack are added to both rental stock pickings after order confirmation.
""",
    "depends": [
        "rental_base",
        "product_pack",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
        "views/product_pack_line_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
