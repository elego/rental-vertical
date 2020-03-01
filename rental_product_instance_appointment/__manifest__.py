# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Instance Appointment',
    'summary': 'Rental Product Instance Appointment',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'rental_product_instance_repair',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'LGPL-3',
}
