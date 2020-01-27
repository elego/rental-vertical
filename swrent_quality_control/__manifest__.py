# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved
{
    'name': 'SW Rental Quality Control',
    'summary': '''Data files of inspection question in quality control for SW Rent.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'website': 'https://gitlab.elegosoft.com/swrent/rental-vertical',
    'depends': [
        'sale_rental',
        'quality_control_stock',
    ],
    'data': [
        'data/test_question_data.xml',
        'views/inspection_line_view.xml',
    ],
    'qweb': [],
    "installable": True,
}