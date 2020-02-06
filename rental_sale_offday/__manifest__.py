# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Off Day',
    'summary': '''This module extends the rental pricelist to calculate the off days''',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'sale_rental_pricelist',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
