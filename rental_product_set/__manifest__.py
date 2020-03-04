# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Set',
    'summary': 'Extends the sale_product_set to add rented product set on sale order lines.',
    'description': '''
Product sets define a number of products that are frequently sold together and are added
as different sale order lines. This modules extends this use case to renting of product
sets. As in the original workflows, independent rental order lines are created for all
the products in the set. There is no further relation between those products.
''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'sale_rental_pricelist',
        'sale_product_set',
        'rental_base',
    ],
    'data': [
        'wizard/product_set_add.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
