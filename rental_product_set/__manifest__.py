# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Set",
    "summary": "Extends the sale_product_set to add rented product set on sale order lines.",
    "description": """
Product sets define a number of products that are frequently sold together and are added
as different sale order lines. This modules extends this use case to renting of product
sets. As in the original workflows, independent rental order lines are created for all
the products in the set. There is no further relation between those products.
""",
    "usage": """
Refer to the usage information of the OCA module sale_product_set to learn how to
define product sets.

This module extends the sale and stock functionality to enable the renting of
OCA product sets. In order to do that, just install the module.

No further configuration is needed.
""",
    "version": "16.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_pricelist",
        "sale_product_set",
        "rental_base",
    ],
    "data": [
        "wizard/product_set_add.xml",
        "views/menu_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
