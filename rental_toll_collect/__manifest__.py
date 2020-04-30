# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Toll Collect',
    'summary': 'Import a CSV file from Toll Collect and distribute the costs\
                to specific rental orders/products/customers',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'product',
        'account',
        'rental_product_instance',
        'contract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/analytic_account_data.xml',
        'views/toll_charge_line_view.xml',
        'views/product_view.xml',
        'views/account_invoice_view.xml',
        'wizard/toll_charge_line_import_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'LGPL-3',
}
