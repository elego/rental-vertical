# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract',
    'summary': 'Extension of module contract.',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Elego Software Solutions GmbH',
    'depends': [
        'contract',
        'product_contract',
        'sale_rental',
        'rental_base',
    ],
    'data': [
        'views/contract_view.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
