# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract',
    'summary':
'''Extension of module contract.
1. set analytic account automatically
2. set date_start and date_end of invoice line automatically
''',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'contract',
        'sale_rental',
        'rental_base',
    ],
    'data': [
        'views/contract_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
