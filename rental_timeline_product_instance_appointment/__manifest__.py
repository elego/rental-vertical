# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Timeline Product Instance Appointment',
    'summary': 'Extends the rental_timeline module to display an appointment icon in the mouse over if there is an appointment during the rental time.',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'description': """
This module adds the display of appointments related to rental products to the rental timeline view.
    """,
    'usage': """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_product_instance_appointment
    """,
    'depends': [
        'rental_timeline',
        'rental_product_instance_appointment',
    ],
    'data': [
        'views/product_timeline_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'AGPL-3',
}
