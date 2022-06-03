# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Rental Routing",
    "summary": "Rental Routing between Rentals",
    "version": "12.0.1.0.2",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "license": "AGPL-3",
    "description": """
Rental products are delivered from the rental_in location of the rental company
to a rental_out location at the renting customer.

This module provides the opportunity to deliver the rental products directly from
customer to customer. After creating a new rental order you can choose a previous
rental as a source. That means, you do not need an outgoing delivery from your
rental location but instead you do a transfer from one customer location to another
customer location.
Depending on the perspective you could also go to the "old" rental and start the
routing there. Then you do not choose a previous rental as source but a following
rental as destination. That means, you do not need an incoming delivery from your
customer's location to your rental location before re-delivering it to the new customer.
You just transfer the product from one customer location to another customer location.
    """,
    "usage": """
TODO
    """,
    "depends": [
        "rental_base",
        "shipment_plan",
        ],
    "data": [
        "wizards/sale_rental_route_view.xml",
        "views/view_order_form.xml",
        "views/sale_rental_view.xml",
        "views/res_partner_view.xml",
        "views/stock_view.xml",
    ],
    "installable": True,
}
