# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Purchase Order Type",
    "summary": "Additional purchase order types for rental use cases: transport orders and repair orders",
    "version": "14.0.1.0.0",
    "category": "Rental/Purchase",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
This module provides the possibility to distiguish purchase orders by the type 'transport' and 'repair' orders', 
using the module purchase_order_type. It also adds new menu entries for transport and repair vendor (purchase) 
orders in the rental application.

Additional order types:
 - Transport Order: used to order transportation for rented products via vehicle, ship or airplane
 - Repair Order: used to order repair work during rental periods
""",
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
