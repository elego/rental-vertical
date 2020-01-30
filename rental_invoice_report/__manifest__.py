# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Report Invoice',
    'version': '12.0.1.0.0',
    'summary': 'Rental Report Invoice',
    'author': 'Elego Software Solutions Gmbh',
    'category': 'Reporting',
    'depends': [
        'account',
        'rental_report_base',
    ],
    'data': [
        'views/account_report.xml',
        'views/report_invoice_template.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
