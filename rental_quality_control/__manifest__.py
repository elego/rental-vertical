# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Quality Control',
    'summary': '''New text field to define the reason for quality failure.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions GmbH',
    'depends': [
        'sale_rental',
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
    'application': True,
    'license': 'AGPL-3',
}
