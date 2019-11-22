# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved
{
    'name': 'SW Rental Extention(SW.Rent)',
    'version': '12.0.1.0.0',
    'license': 'Other proprietary',
    'category': 'Rental Management',
    'author': 'Elegosoft',
    'website': 'https://gitlab.elegosoft.com/swrent/rental-vertical',
    'depends': [
        'fieldservice_account',
        'fieldservice_maintenance',
        'fieldservice_repair',
        'fieldservice_stock',
        'purchase',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/account_invoice_view.xml',
        'views/stock_move_view.xml',
        'views/repair_order_view.xml',
        'views/purchase_order_view.xml',
    ],
    'qweb': [],
    "installable": True,
}
