# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Base',
    'summary':
'''Base Module for Rental.
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'crm',
        'product_analytic',
        'purchase',
        'sale_order_type',
        'sale_rental',
        'repair',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/order_type_data.xml',
        'views/res_config_settings_view.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
