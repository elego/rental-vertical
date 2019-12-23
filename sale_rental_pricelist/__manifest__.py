# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Rental Pricelist',
    'summary': '''This module enable the user to define different rental price with time uom ("Month", "Day" and "Hour").''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'sale_rental',
    ],
    'data': [
        'data/product_uom_data.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
