# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Menu CRM',
    'summary': 'Add CRM to the Rental Menu',
    'description':
'''
This module just adds menu extenions to the rental application.
''',
    'usage':
'''
just install
''',
    'version': '12.0.1.0.1',
    'category': 'Rental/CRM',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'crm',
    ],
    'data': [
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
