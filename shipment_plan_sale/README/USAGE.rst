
Usage
-----

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

