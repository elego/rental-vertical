# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Variant',
    'summary':
'''Model Product is extended with rental special fields.''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
