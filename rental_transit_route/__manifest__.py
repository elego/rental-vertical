# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Transit Route',
    'summary': 'Rental Transit Route',
    'version': '12.0.1.0.0',
    'category': 'stock',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
    ],
    'data': [
        'data/route_data.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
}
