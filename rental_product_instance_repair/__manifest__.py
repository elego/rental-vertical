# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Instance Repair',
    'summary': 'Extension of module rental_product_instance and rental_repair',
    'version': '12.0.1.0.0',
    'category': 'Rental/Service',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'usage': """
This module is automatically installed when all of the following modules are installed in a database:

- rental_repair
- rental_product_instance
    """,
    'depends': [
        'rental_repair',
        'rental_product_instance',
    ],
    'data': [
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'AGPL-3',
}
