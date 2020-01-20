# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Rental Timeline',
    'summary': '''This module extends the sale_rental module to create/change the
timeline object for the rented product instance automatically.
A Timeline View will be generated for all the related products.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'web_timeline',
        'sale_rental',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/product_timeline_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
