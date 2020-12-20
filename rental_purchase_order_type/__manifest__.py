# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Purchase Order Type",
    "summary": "Additional purchase order types for rental use cases: transport orders and repair orders",
    "description": """
This module provides the possibility to distiguish purchase orders by the type 'transport' and 'repair' orders', 
using the module purchase_order_type. It also adds new menu entries for transport and repair vendor (purchase) 
orders in the rental application.

Additional order types:
 - Transport Order: used to order transportation for rented products via vehicle, ship or airplane
 - Repair Order: used to order repair work during rental periods
""",
    "usage": """
- Install the module.
- Create a purchase order as a transport order here: Rental > Vendors > Transport Order.
- Create a purchase order as a repair order here: Rental > Vendors > Repair Order.
- Create a purchase order and set manually the purchase order type as desired.
    """,
    "version": "12.0.1.0.0",
    "category": "Rental/Purchase",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
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
    "license": "AGPL-3",
}
