# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Shipment Management',
    'summary': 'Stock Shipment Management',
    'version': '12.0.1.0.0',
    'category': 'Transportation',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'rental_transit_route',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/shipment_plan.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
