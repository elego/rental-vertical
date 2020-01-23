# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Quality Control',
    'summary': '''New text field to define the reason for quality failure.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'website': 'https://gitlab.elegosoft.com/swrent/rental-vertical',
    'depends': [
        'sale_rental',
        'quality_control_stock',
    ],
    'data': [
        'views/inspection_line_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}