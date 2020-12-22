# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Reporting",
    "summary": "Add rental-specific reporting menu and functions",
    "description": """
This module adds rental-specific reporting to the rental application.
Currently, this ist still just a menu :-(
The actual reporting is still missing.
""",
    "usage": """
just install
""",
    "version": "12.0.1.0.1",
    "category": "Rental/Reporting",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_base",
        "mis_builder",
    ],
    "data": [
        "views/menu_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
