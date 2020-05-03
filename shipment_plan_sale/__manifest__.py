# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Shipment Plan',
    'summary': 'Sale Shipment Plan',
    'version': '12.0.1.0.0',
    'category': 'Transportation',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'shipment_plan',
    ],
    'data': [
        'wizard/create_transport_request_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/shipment_plan_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'license': 'AGPL-3',
}
