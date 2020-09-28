# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract Insurance',
    'summary': 'Rental Contract Insurance',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_contract_month',
        'rental_product_insurance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        #TODO add data to set visible group of uom
        'data/contract_template_data.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'AGPL-3',
}
