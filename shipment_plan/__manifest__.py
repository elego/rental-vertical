# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Shipment Management",
    "summary": "Shipment Management",
    "version": "12.0.1.0.0",
    "category": "Transportation",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "description": """
This module provides the base of the shipment management in order to organize and manage transportation
for products that are to voluminous or heavy or somehow dangerous, and therefore need special transport treatment.
The shipment plans focus on the transport after leaving or before entering the internal stock locations.
    """,
    "usage": """
Configure the storable products that need transportation.
 - Set the product type to 'Storable Product'.
 - Set the flag 'Transport required' (trans_purchase_request) to True.

Configure transport services that can be purchased from delivery carriers.
 - Set the product type to 'Service'.
 - Set the flag 'Transport Service' (is_transport) to True.
 - Go to Page 'Purchase' amd add some suppliers that offer this transport service.
 - Also choose the 'Transport Service Type' in order to create a purchase order or a call for tender.

Configure the granularity of transport costs.
 - Go to Inventory > Configuration > Settings
 - Choose the transport cost type as single or multiple positions.
 Choosing the cost type 'Multi Positions’ the transport purchase order or call for tender can contain several lines
 for the different costs related to the transport, e.g. the transport costs itself and several charges.
 You can define the appropriate transport services when creating a new transport request.
 Choosing the cost type 'Single Position’ the transport request will only consist of one line with all costs.

Create a new shipment plan and purchase requests.
 - Go to Inventory > Operation > Shipment Plans.
 - Choose the starting address and the destination address.
 - Set the estimated time or arrival and departure.
 - Give some more description that the transport carrier will need.
 - Create a new purchase request by button click.
 - Choose the transport service.
 - Choose the request type to be either a purchase order or requisition (tender).
 - Create a purchase order or requistion.
 - Use these purchase orders as usual.

 Create a shipment plan for internal pickings.
  - Go to Inventory > Configuration > Settings and activate multiple storage locations.
  - Go to Inventory > Operation > Transfers.
  - Create a new stock picking with internal picking type.
  - Create a shipment plan for this internal transfer, which is then linked in a smartbutton.
    """,
    "depends": [
        "purchase",
        "purchase_requisition",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/create_transport_request_view.xml",
        "views/shipment_plan.xml",
        "views/product_view.xml",
        "views/purchase_view.xml",
        "views/stock_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
