# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Instance',
    'summary': 'Add product instances identified by serial number as unique rented objects',
    'description':
'''Model product is extended as an instance that can be traced by serial number.
An instance can only have one serial number, so that it is unique in the system.
It can be used in rental orders, repair orders and maintenance orders.''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_product_variant',
        'sale_rental_timeline',
    ],
    'data': [
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
