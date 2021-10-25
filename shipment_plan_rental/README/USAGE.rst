
Usage
-----

Configure storable and service products as described in module 'shipment_plan'.

Configure these storable products as rental products.
 - Set the boolean field 'Rental' to True.
 - Please also install rental_pricelist to easily create the related rental services for daily or monthly rentals
   or do it manually as described in module 'sale_rental'.

Configure incoterms as described in module 'shipment_plan_sale'.

Create a rental order for a product that needs transportation.
 - Go to Rentals > Customer > Rental Quotations.
 - Create a new rental quotation.
 - Choose a customer.
 - Choose an incoterm configured to allow the creation of a transport request.
 - Add a storable and rentable product that needs transportation.
 - Save the order.
 - Click the button 'Request Transport'.
 - Choose the transport service that should be used in the purchase order / requisition.
 - Create the request.
 - Check both shipment plans, purchase requisitions and/or purchase orders for outbound and inbound transport.

