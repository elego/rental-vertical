# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Task Order',
    'summary': 'Project Task Order',
    'version': '12.0.1.0.0',
    'category': 'project',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'project',
        'product_analytic',
        'rental_product_instance',
    ],
    'data': [
        'views/project_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
