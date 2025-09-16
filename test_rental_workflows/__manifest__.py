# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Test Rental Workflows',
    'summary': 'Test Rental Workflows',
    'description': '''
Test Rental Workflows
''',
    'version': "18.0.1.0.0",
    'category': 'Tests',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'web',
        'web_tour',
        'sale_rental',
        'rental_base',
        'rental_config',
        'rental_dashboard',
        'rental_pricelist',
        'rental_product_set',
        'rental_product_instance',
        'rental_product_variant',
        'rental_offday',
        'rental_contract_month',
        'rental_contract_toll_collect',
        'rental_timeline',
        'rental_toll_collect',
        'quality_control_stock_oca',
        'rental_routing',
        'rental_repair',
    ],
    'data': [
        'data/settings.xml',
    ],
    'demo': [
        'demo/rental_products.xml',
        'demo/inventory.xml',
        'demo/quality_control_data.xml',
        'demo/toll.charge.line.csv',
    ],
    'qweb': [
    ],
    "assets": {
        'web.assets_backend': [
            "/test_rental_workflows/static/src/js/test_rental_tour.js",
            "/test_rental_workflows/static/src/js/test_rental_contract_tour.js",
            "/test_rental_workflows/static/src/js/test_rental_return_product_qc_tour.js",
            "/test_rental_workflows/static/src/js/test_rental_toll_collect_tour.js",
            "/test_rental_workflows/static/src/js/test_rental_contract_toll_collect_tour.js",
        ],
    },
    'installable': True,
    'license': 'AGPL-3',
}
