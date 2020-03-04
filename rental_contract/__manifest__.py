# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract',
    'summary': 'Extension of module contract for rental use cases',
    'description': '''
During longtime rentals, it is often required to write invoices in regular intervals.
This is possible with the contract module, which is here extended to support rental
use cases in extension to purchase and sale use cases.
''',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'contract',
        'product_contract',
        'sale_rental',
        'rental_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/default_type_data.xml',
        'data/contract_template_data.xml',
        'views/contract_view.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
        'views/contract_order_type_view.xml',
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
