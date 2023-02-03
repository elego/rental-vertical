# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Purchase Sale Rental Intercompany",
    "summary": "Purchase Sale Rental Intercompany",
    "description": "Purchase Sale Rental Intercompany",
    "usage": "Purchase Sale Rental Intercompany",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "purchase_sale_inter_company",
        "purchase_start_end_dates",
        "purchase_order_type",
        "sale_start_end_dates",
        "sale_order_type",
    ],
    "data": [
        "security/security.xml",
        "views/sale_order_type_view.xml",
        "views/purchase_order_type_view.xml",
        "views/purchase_order_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
