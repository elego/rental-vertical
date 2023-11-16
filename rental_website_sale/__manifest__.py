# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Website Sale",
    "summary": "Extends eCommerce.",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module removes the add to card button and product quantity spinner from the webshop product detail
page. It also shows more details and information of the product. 
    """,
    "usage": """
This module is automatically installed.
    """,
    "depends": [
        "website_sale",
        "rental_product_instance",
    ],
    "data": [
        "views/templates.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
