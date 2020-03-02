# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Base',
    'summary': 'Base module for rental use cases',
    'description':
'''Base Module for Rental Support

This module add some basic configuration options and extensions for rental use cases.

Configuration options:
 - Price Extension: set rental price with different unit of measure.
 - Off Days: use and calculate the off-days for rental periods which are not billed
 - Timelines: use timelines for rental product
 - Product Pack: allow renting of product packs
 - Product Variant: allow renting of product variants
 - Product Instance: rent unique product instances with serial numbers
 - Product Set: allow renting of product sets
 - Contract: allow use of contracts for renting
 - Repair Order: support repair orders during renting
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
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
        'views/stock_picking_views.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
