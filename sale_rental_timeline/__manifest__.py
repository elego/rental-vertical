# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Rental Timeline',
    'summary': '''This module extends the sale_rental module to create/change the
timeline object for the rented product instance automatically.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'swrent_product_extension',
    ],
    'data': [
        #'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
