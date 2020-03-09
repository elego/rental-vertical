# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Invoice',
    'summary': '''Rental Invoice''',
    'description':
'''This module add the 2-phase confirmation of incoming invoices including delegated charging to customers.
''',
    'version': '12.0.1.0.0',
    'category': 'Purchase Management',
    'author': 'Elego Software Solutions GmbH',
    'depends': [
        'purchase',
    ],
    'data': [
        'data/groups.xml',
        'wizard/create_customer_invoice_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
