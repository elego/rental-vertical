# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rental Product Variant',
    'summary':
'''Model Product is extended with rental special fields.''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'rental_base',
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
