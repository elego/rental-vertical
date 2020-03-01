# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Purchase Order Type',
    'summary': 'Additional purchase order types for rental use cases: transport orders and repair orders',
    'description': '''
Additional order types:
 - Transport Order: used to order transportation for rented products via vehicle, ship or airplane
 - Repair Order: used to order repair work during rental periods
''',
    'version': '12.0.1.0.0',
    'category': 'Purchase Management',
    'author': 'OCA/Elego Software Solutions GmbH',
    'depends': [
        'purchase_order_type',
        'rental_base',
    ],
    'data': [
        'data/purchase_order_type.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'LGPL-3',
}
