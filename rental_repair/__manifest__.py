# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Repair",
    "summary": "Support repair orders during rental periods",
    "description": """
""",
    "version": "15.0.1.0.0",
    "category": "Rental/Service",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "project",
        "rental_base",
        "repair",
        "rental_purchase_order_type",
        "rental_product_instance",
    ],
    "data": [
        "data/project_data.xml",
        "security/security.xml",
        "views/project_view.xml",
        "views/product_view.xml",
        "views/purchase_views.xml",
        "views/repair_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
