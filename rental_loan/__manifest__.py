# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Loan',
    'summary': 'Extension of module action_loan for rental use cases',
    'description': '',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'account_loan',
        'rental_base',
    ],
    'data': [
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'AGPL-3',
}
