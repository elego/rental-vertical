# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Test Rental Workflows',
    'summary': 'Test Rental Workflows',
    'description': '''
Test Rental Workflows
''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        # 'sale',
        'web',
        'web_tour',
        'sale_rental',
        'rental_base',
        'rental_pricelist',
        'rental_product_set',
        'rental_product_instance',
    ],
    'data': [
        'data/settings.xml',
        'views/assets.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
