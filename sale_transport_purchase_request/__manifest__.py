# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Transport Purchase Request',
    'summary': 'Sale Transport Purchase Request',
    'version': '12.0.1.0.0',
    'category': 'purchase',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'account',
        'purchase',
        'purchase_requisition',
        'sale',
    ],
    'data': [
        'data/product_data.xml',
        'wizard/create_transport_request_view.xml',
        'views/account_incoterms_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'views/res_config_settings_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'license': 'LGPL-3',
}
