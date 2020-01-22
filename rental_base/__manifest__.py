# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rental Base',
    'summary':
'''Base Module for Rental.
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
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
    'license': 'AGPL-3',
}
