# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Insurance',
    'summary': 'Sell Insurance of Product',
    'description': '''
This module provides the opportunity to sell and invoice insurances related to the selled and invoiced rentable products.
The insurance price is either based on the product's costs or the order's amount and given as percentage.
''',
    'usage': '''
- Install the module.
- Open a rentable product and go to page Sale.
- Choose the calculation method for the insurance when renting this product and set the percentage.
- Create a sale order.
- Add a line with a product and see the default settings for the insurance.
- Save the sale order and see the newly added line for the insurance with the calculated price.
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
    ],
    'data': [
        'data/product_data.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
