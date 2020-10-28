# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Menu CRM',
    'summary': 'Add CRM to the Rental Menu',
    'description': '''
This module adds menu entries for CRM to the rental application.
    ''',
    'usage': '''
- Install the module.
- See new menu entries for CRM in rental application.
    ''',
    'version': '12.0.1.0.1',
    'category': 'Rental/CRM',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
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
