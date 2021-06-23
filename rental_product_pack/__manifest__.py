# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Pack",
    "summary": "Allow use of product packs as in rental use cases",
    "description": """
With this module, product packs can be rented as one compound product. Throughout the
renting process, this compound product will be handled as one entity.
""",
    "usage": """
Refer to the usage information of the OCA module product_pack to learn how to
define product packs.

This module extends the sale and stock functionality to enable the renting of
OCA product packs. In order to do that, just install the module.

No further configuration is needed.
""",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_base",
        "product_pack",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pack_line_views.xml",
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
