# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Transport Purchase Request',
    'summary': 'Rental Transport Purchase Request',
    'version': '12.0.1.0.0',
    'category': 'purchase',
    'author': 'OCA/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
        'purchase_requisition',
    ],
    'data': [
        'data/product_data.xml',
        'views/account_incoterms_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'license': 'LGPL-3',
}
