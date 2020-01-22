# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
    'license': 'AGPL-3',
}
