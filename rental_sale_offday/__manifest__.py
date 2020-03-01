# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Off Day',
    'summary': 'Extends the rental pricelists to calculate the off-days',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'OCA/Elego Software Solutions GmbH',
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
