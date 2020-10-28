# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Timeline Product Instance',
    'summary': 'Extends the rental_timeline module to show the product instance fields in the timeline product popup.',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'usage': """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_product_instance
    """,
    'depends': [
        'rental_timeline',
        'rental_product_instance',
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
