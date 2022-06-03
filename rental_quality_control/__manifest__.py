# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Quality Control",
    "summary": "New text field to define the reason for quality failure.",
    "description": """
This module extends the quality_control_stock module to add a reason
for failure during quality control, Inspections count smart button on Product form view
and two Quality Control menus under Rental/Customers/Delivery for Customers and
Rental/Vendor/Delivery for the Vendors.""",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "sale_rental",
        "quality_control_stock",
        "rental_base",
    ],
    "data": [
        "views/inspection_line_view.xml",
        "views/product_view.xml",
        "views/menu_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
