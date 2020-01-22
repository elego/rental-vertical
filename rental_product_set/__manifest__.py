# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rental Product Set',
    'summary': '''This module extends the sale_product_set to add rented product set on sale order line.''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elegosoft',
    'depends': [
        'sale_rental_pricelist',
        'sale_product_set',
    ],
    'data': [
        'wizard/product_set_add.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
