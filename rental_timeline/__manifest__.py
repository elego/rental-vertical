# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline",
    "summary": "Adds a timeline to products as well as a timeline view as overview of all rental products and orders",
    "description": """
This module extends the sale_rental module to create and change the timeline objects
for the rented product instances automatically.
A complete timeline view containing all rental orders will be generated for all rentable products.

This module adds the basic rental timeline view as well as an extension to the product form view.
    """,
    "usage": """
Just install this module to add the rental timeline view to your system. No further configuration is necessary.
    """,
    "version": "18.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "web_timeline",
        "rental_base",
        "rental_product_variant",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/rental_timeline_templates.xml",
        "views/product_timeline_view.xml",
        "views/product_view.xml",
    ],
    'qweb': ['static/src/js/timeline_renderer.xml'],
    "demo": [],
    "assets": {
        'web.assets_backend': [
            "web_timeline/static/src/**/*",
            "rental_timeline/static/src/scss/rental_timeline.scss",
            "rental_timeline/static/src/js/Popup.js",
            "rental_timeline/static/src/js/rental_timeline_arch_parser.esm.js",
            "rental_timeline/static/src/js/timeline_model.esm.js",
            "rental_timeline/static/src/js/timeline_renderer.esm.js",
            "rental_timeline/static/src/js/timeline_controller.xml",
            "rental_timeline/static/src/js/timeline_controller.esm.js",
            "rental_timeline/static/src/js/timeline_view.esm.js",
        ],
    },
    "application": False,
    "license": "AGPL-3",
}
