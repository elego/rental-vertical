# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Check Availability",
    "summary": "Extends the sale_rental module for checking availability of the rented product.",
    "version": "16.0.1.0.0",
    "category": "Rental",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
This module activates availability checks on stockable products related to rental services in
sale orders. In the base functionality only the total amount of products in stock is checked and user is
informed when the amount of products to rent out in a sale order is higher.

After the installation of this module the availability is checked in consideration of the total amount
of goods in stock and the amount of products used in concurrent sale orders at the certain desired timeframe.
In case of insufficient products in stock the user receives visual notification on respective sale order line
and can access the list of concurrent sale orders directly.
""",
    "contributors": [
        "Ben Brich <b.brich@humanilog.org> (www.humanilog.org)",
        "Yu Weng <yweng@elegosoft.com> (www.elegosoft.com)",
    ],
    "depends": [
        "rental_pricelist",
    ],
    "data": [
        "views/sale_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
