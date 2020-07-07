# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Pack',
    'summary': 'Allow use of product packs as in rental use cases',
    'description': '''
With this module, product packs can be rented as one compound product.
''',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
        'product_pack',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
