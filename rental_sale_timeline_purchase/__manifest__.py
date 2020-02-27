# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Sale Timeline Purchase',
    'summary': '''This module extends the sale_rental_timeline module to show the transport order fields in the timeline popup.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'sale_rental_timeline',
        'rental_transport_purchase_request',
    ],
    'data': [
        'views/product_timeline_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
