# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Off-Day",
    "summary": "Manage off-days in rentals on daily basis",
    "version": "15.0.1.0.0",
    "category": "Rental",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
During short-term rentals over several days or weeks, the customer and the salesman
agree on so called off-days. On these days the customer still have the rented products
but usually doesn't use them and, therefore, does not pay the daily price. This is often
the case for weekends and holidays, since there might be some legal limitations in using
the products on these days.
In order to meet this requirement, the salesman can add off-days on sale order lines for
products that are rentable in days. These days will not be included in price calculation.
""",
    "depends": [
        "rental_pricelist",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": False,
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
