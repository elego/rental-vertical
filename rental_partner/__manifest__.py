# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Partner',
    'summary': 'Rental Partner',
    'description': '''
Customize Partner form view
''',
    'usage': '''
Customize Partner form view
''',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'partner_firstname',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'LGPL-3',
}
