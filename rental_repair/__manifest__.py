# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Repair',
    'summary': 'Support repair orders during rental periods',
    'description': '''
''',
    'version': '12.0.1.0.0',
    'category': 'project',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'project',
        'rental_base',
        'repair',
        'rental_purchase_order_type',
    ],
    'data': [
        'data/project_data.xml',
        'views/project_view.xml',
        'views/product_view.xml',
        'views/repair_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'LGPL-3',
}
