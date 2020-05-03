# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Shipment Management',
    'summary': 'Shipment Management',
    'version': '12.0.1.0.0',
    'category': 'Transportation',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'account',
        'purchase',
        'purchase_requisition',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_transport_request_view.xml',
        'views/shipment_plan.xml',
        'views/account_incoterms_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
