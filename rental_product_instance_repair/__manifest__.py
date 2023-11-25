# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Instance Repair",
    "summary": "Extension of module rental_product_instance and rental_repair",
    "description": """
This module extends the modules rental_repair and rental_product_instance.
It adds a smartbutton to the product form view of product instances to get
an overview of all related project tasks.
It automatically sets the serial number of a product instance in project tasks and repair orders.
    """,
    "usage": """
- Install the module.
- Go to the product form view of a product instance and check the new smartbutton.
- Change the product in tasks or repair orders and see the onchange event for the serial number.
    """,
    "version": "15.0.1.0.0",
    "category": "Rental/Service",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- rental_repair
- rental_product_instance
    """,
    "depends": [
        "rental_repair",
        "rental_product_instance",
    ],
    "data": [
        "views/project_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
