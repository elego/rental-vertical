# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Rental Routing",
    "summary": "This module adds support for the management of transports of rental products.",
    "version": "12.0.1.0.2",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "license": "AGPL-3",
    "description": """
Rental products are deliverd from the rental_in location of the rental company
to a rental_out location at the renting customer.

This module adds the following fields and views:

TODO

    """,
    "usage": """
TODO
    """,
    "depends": ["rental_base"],
    "data": [
        "wizards/sale_rental_route_view.xml",
        "views/view_order_form.xml",
        "views/sale_rental_view.xml",
        "views/res_partner_view.xml",
        "views/stock_view.xml",
    ],
    "installable": True,
}
