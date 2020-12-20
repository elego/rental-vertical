# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Offday",
    "summary": "Extends the rental_timeline module to show the offday_number in the timeline popup.",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module adds the display of the number of 'offdays' in rental orders to the rental timeline view.
'offdays' are days that are not invoiced within the renting period, for example weekends or holidays.
    """,
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_offday

No further configuration is needed.
    """,
    "depends": [
        "rental_timeline",
        "rental_offday",
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
