# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Insurance',
    'summary': 'Sell Insurance of Product',
    'description': '''
With this module, product insurance can be sold as service.
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
    ],
    'data': [
        'data/product_data.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
