# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Rental Menu',
    'summary': '''This module shows the main menus for sale rental''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'account',
        'purchase',
        'maintenance',
        'stock',
        'swrent_product_extension',
        'sale_rental',
        'sale_order_type'
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/order_type_data.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'license': 'AGPL-3',
}
