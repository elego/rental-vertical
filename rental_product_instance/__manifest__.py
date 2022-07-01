# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Instance",
    "summary": "Add product instances identified by serial number as unique rented objects",
    "description": """
This module extends the product data model in order to mark them as unique product instances 
that are traced by serial number. You might have several instances of a product but they are 
in different conditions or are somehow unique like machines, vehicles or maybe 'used' products.

In order to track the condition history of a product instance you can add operating data, e.g.
you can save the mileage of vehicles or the operating hours of machines.
    """,
    "usage": """
- Install the module.
- Create a stockable product.
- Mark the product as product instance.
- Save the product and set an unique serial number.
  Hint: Make an inventory adjustment, if needed.
- Set a product category that can be configured to either use mileage or operating hours as condition.
- Go to the smartbutton for operating data, create the current condition and update it regularly.
    """,
    "version": "12.0.1.0.1",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_product_variant",
        "product_template_tags",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
        "views/instance_operating_data_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
