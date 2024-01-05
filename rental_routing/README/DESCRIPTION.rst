Rental Routing
====================================================

*This file has been generated on 2023-02-19-14-17-56. Changes to it will be overwritten.*

Summary
-------

This module adds support for the management of transports of rental products.

Description
-----------

Rental products are delivered from the rental_in location of the rental company
to a rental_out location at the renting customer.

This module provides the opportunity to deliver the rental products directly from
customer to customer. After creating a new rental order you can choose a previous
rental as a source. That means, you do not need an outgoing delivery from your
rental location but instead you do a transfer from one customer location to another
customer location.
Depending on the perspective you could also go to the "old" rental and start the
routing there. Then you do not choose a previous rental as source but a following
rental as destination. That means, you do not need an incoming delivery from your
customer's location to your rental location before re-delivering it to the new customer.
You just transfer the product from one customer location to another customer location.

