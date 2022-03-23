# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Purchase Order Type",
    "summary": "Additional purchase order types for rental use cases: transport orders and repair orders",
    "version": "14.0.1.0.0",
    "category": "Rental/Purchase",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "depends": [
        "purchase_order_type",
        "rental_base",
    ],
    "data": [
        "data/purchase_order_type.xml",
        "views/menu_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
