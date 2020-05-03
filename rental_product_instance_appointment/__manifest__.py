# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Instance Appointment',
    'summary': 'Rental Product Instance Appointment',
    'description': '''
Product instances are unique products in a current state and some tasks needs to be regularly done with them.
This module provides the possibility to add single or recurrent appointments for a product which automatically
create project tasks a defined time before the actual appointment date.
''',
    'usage': '''
- Create a product instance.
- Add one or several appointments in 'Appointments' page on product view.
- Set a name, date, a notification lead time and a time interval for each appointment.

The cron job 'Update product appointments daily' will check all product instances, 
create related project tasks in helpdesk project and update the due date for the next appointments.
''',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
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
    'license': 'AGPL-3',
}
