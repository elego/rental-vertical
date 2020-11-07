# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Rental Forward Shipment Plan',
    'summary': 'Rental Routing Shipment Plan',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'license': 'AGPL-3',
    'description': '''
Usually, rental products are deliverd from the rental_in location of the rental company
to a rental_out location at the renting customer. However, this can be optimized in
certain situations, when it is more appropriate to ship the product from one customer
to the next customer.
    ''',
    'usage': '''
TODO

This module is automatically installed when all of the following modules are installed in a database:

- rental_routing
- shipment_plan_rental
    ''',
    'depends': [
        "rental_routing",
        "shipment_plan_rental",
    ],
    'data': [
        "views/shipment_plan_view.xml",
    ],
    'installable': True,
    'auto_install': True,
}
