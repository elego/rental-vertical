# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Report Sale',
    'version': '12.0.1.0.0',
    'summary': 'Rental Report Sale',
    'author': 'Elego Software Solutions Gmbh',
    'category': 'Reporting',
    'description': """
        This module provides a customized sale report.
        """,
    'depends': [
        'sale',
        'rental_report_base',
    ],
    'data': [
        'report/sale_report.xml',
        'report/sale_report_templates.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
