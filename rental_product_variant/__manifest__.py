# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'SWRent Product Extension',
    'summary':
'''Model Product is extended as an Instance, that can be traced by serial number.
   An Instance can only has one serial number, so that it is unique in the system.
   It can be used in Rental Order, Repair Order and Maintenance Order''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'account',
        'maintenance',
        'purchase',
        'repair',
        'sale',
        'sale_rental',
        'sale_rental_timeline',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
