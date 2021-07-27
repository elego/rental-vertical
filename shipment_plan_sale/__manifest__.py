# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Shipment Management Sale",
    "summary": "Shipment Management Sale",
    "version": "12.0.1.0.0",
    "category": "Sale/Transportation",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module provides the base of the shipment management in order to organize and manage transportation
for products that are to voluminous or heavy or somehow dangerous, and therefore need special transport treatment.
The shipment plans focus on the transport after leaving or before entering the internal stock locations.

This module provides a sale extension for the shipment management.
The combination of a storable product that needs transportation and the use of an incoterm configured for outbound
transportation allows the salesmen to create a transport request (purchase order or requisition) directly from the
sale order. It will also create the shipment plan.
    """,
    "usage": """
Configure storable and service products as described in module 'shipment_plan'.

Configure incoterms that should allow the creation of transport requests from sale orders.
 - Go to Invoicing > Configuration > Incoterms
 - Set the field 'Outbound transport required' (trans_pr_needed) to True.

Create a sale order for a product that needs transportation.
 - Go to Sales > Orders > Quotations.
 - Create a new quotation.
 - Choose a customer.
 - Choose an incoterm configured to allow the creation of a transport request.
 - Add a storable product that needs transportation.
 - Save the order.
 - Click the button 'Request Transport'.
 - Choose the transport service that should be used in the purchase order / requisition.
 - Create the request.
 - Check the shipment plan, purchase requisition and/or purchase orders.
    """,
    "depends": [
        "shipment_plan",
        "sale_management",
        "sale_start_end_dates",
        "stock",
    ],
    "data": [
        "data/res_config_settings_data.xml",
        "wizard/create_transport_request_view.xml",
        "views/account_incoterms_view.xml",
        "views/product_view.xml",
        "views/sale_view.xml",
        "views/shipment_plan_view.xml",
        "views/stock_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "license": "AGPL-3",
}
