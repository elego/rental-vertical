# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Reporting",
    "summary": "Add rental-specific reporting menu and functions",
    "version": "16.0.1.0.0",
    "category": "Rental/Reporting",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
This module adds rental-specific reporting to the rental application.
Currently, this ist still just a menu :-(
The actual reporting is still missing.
""",
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
    "installable": True,
    "license": "AGPL-3",
}
