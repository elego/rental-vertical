# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Set',
    'summary': '''This module extends the sale_product_set to add rented product set on sale order line.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'sale_rental_pricelist',
        'sale_product_set',
    ],
    'data': [
        'wizard/product_set_add.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
