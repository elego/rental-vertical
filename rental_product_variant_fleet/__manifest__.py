# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Variant Fleet",
    "summary": "Extends model product with fields,related to fleet and vehicle specific.",
    "description": """
This module adds several fields to the product form.

Additional fields:
 - fleet_type_id [Many2one]: fleet.type -- fleet type

Additional fields configured and added by product category:
 - Show Vehicle Identification Number -> vehicle_number [Char]: vehicle identification number
 - Show License Plate -> license_plate [Char]: license plate
 - Show Initial Registration -> init_regist [Date]: date of initial registration
""",
    "usage": """
In order to get vehicle related fields, open the product category and activate the desired checkboxes.
""",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_product_variant",
        "rental_product_instance",
        "rental_timeline_product_instance",
    ],
    "data": [
        # "security/ir.model.access.csv", need to add later
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "auto_install": True,
    "license": "AGPL-3",
}
