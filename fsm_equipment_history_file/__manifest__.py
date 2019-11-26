# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Field Service Equipment History File',
    'summary': 'Manage Field Service Equipment History File',
    'version': '12.0.1.0.0',
    'category': 'Field Service',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/field-service',
    'depends': [
        'mrp',
        'fieldservice_stock',
        'sw_rental_extention',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        #'security/ir_rule.xml',
        #'views/res_config_settings.xml',
        'views/product_view.xml',
        'views/fsm_equipment_view.xml',
        'views/fsm_equipment_history_file_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
