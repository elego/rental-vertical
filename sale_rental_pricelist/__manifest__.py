# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Rental Pricelist',
    'summary': '''This module enable the user to define different rental price with time uom ("Month", "Day" and "Hour").''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'rental_base',
    ],
    'data': [
        'data/product_uom_data.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
