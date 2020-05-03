# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Shipment Plan Rental',
    'summary': 'Shipment Plan for Rental',
    'version': '12.0.1.0.0',
    'category': 'purchase',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'shipment_plan_sale',
        'rental_base',
    ],
    'data': [
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'license': 'AGPL-3',
}
