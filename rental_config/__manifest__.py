# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Config",
    "summary": "Rental Config simplifies rental module installation",
    "version": "15.0.1.0.0",
    "category": "Rental",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://gitlab.elegosoft.com/swrent/rental-vertical",
    "description": """
Rental Config

This module add some basic configuration options for rental use cases.

Configuration options:
 - Rental Prices: Rental prices can be configured for hourly, daily or monthly rentals.
 - Rental Off-Days: Off-days can be calculated for daily rentals which are excluded from price calculation.
 - Timeline: Use timeline for order regarding a rental product.
 - Rental Product Pack: Rental orders for product packs will also update the stock of pack components.
 - Product Variant: Configure rental products with extended fields and smartbuttons.
 - Product Instance: Use a product as unique product instance with serial number.
 - Product Set: Rental products can be grouped in a set for usage in rental orders.
 - Contract: Rental contracts are automatically created from monthly rentals for periodic invoicing.
 - Repair Order: Support repair orders for product instances.
""",
    "depends": [
        "rental_base",
    ],
    "data": [
        "views/res_config_settings_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
