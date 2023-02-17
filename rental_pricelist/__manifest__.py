# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Pricelist",
    "summary": "Enables the user to define different rental prices with "
    "time uom (Month, Day and Hour).",
    "version": "16.0.1.0.0",
    "category": "Rental",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
Rental prices are usually scaled prices based on a time unit, typically day, sometimes months or hour.
This modules integrates the standard Odoo pricelists into rental use cases and allows the user an
easy way to specify the prices in a product tab as well as to use all the enhanced pricelist features.
""",
    "depends": [
        "rental_base",
    ],
    "data": [
        "views/sale_view.xml",
        "views/product_view.xml",
        "views/res_company_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_init_hook": "set_multi_sales_price",
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
