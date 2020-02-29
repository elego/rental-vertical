# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Set',
    'summary': '''This module extends the sale_product_set to add rented product set on sale order lines.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'OCA/Elego Software Solutions GmbH',
    'depends': [
        'sale_rental_pricelist',
        'sale_product_set',
        'rental_base',
    ],
    'data': [
        'wizard/product_set_add.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
