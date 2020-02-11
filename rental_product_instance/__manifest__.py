# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Instance',
    'summary':
'''Model Product is extended as an Instance, that can be traced by serial number.
   An Instance can only has one serial number, so that it is unique in the system.
   It can be used in Rental Order, Repair Order and Maintenance Order''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Elego Software Solutions GmbH',
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
