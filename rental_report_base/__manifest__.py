# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Report Base',
    'version': '12.0.1.0.0',
    'summary': 'Rental Report Base',
    'author': 'Elego Software Solutions Gmbh',
    'category': 'Reporting',
    'description': """
        This module provides a customized external layout.
        """,
    'depends': [
        'web',
        'account',
    ],
    'data': [
        'views/report_template.xml',
        'data/report_layout.xml',
        'data/system_settings.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
