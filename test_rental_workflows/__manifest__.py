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
        'web',
        'web_tour',
        'sale_rental',
        'rental_base',
        'rental_pricelist',
        'rental_product_set',
        'rental_product_instance',
        'rental_product_variant',
        'rental_offday',
        'rental_contract_month',
        'rental_timeline',
        'quality_control_stock',
    ],
    'data': [
        'data/settings.xml',
        'views/assets.xml',
    ],
    'demo': [
        'demo/rental_products.xml',
        'demo/inventory.xml',
        'demo/quality_control_data.xml',
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
