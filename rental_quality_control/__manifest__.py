# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Quality Control',
    'summary': 'New text field to define the reason for quality failure.',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_sale',
        'quality_control_stock',
    ],
    'data': [
        'views/inspection_line_view.xml',
        'views/product_view.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
