Rental Routing
====================================================

*This file has been generated on 2022-05-04-12-21-41. Changes to it will be overwritten.*

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


Usage
-----

TODO


Changelog
---------

- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 4f834448 2022-03-23 12:22:21 +0100 cpatel@elegosoft.com  (origin/feature_4516_blp544_add_files_ported_from_v12_v14) [IMP] rental_return_product_qc tour correction, (issue#4516)
- 279539a5 2022-03-14 10:48:31 +0100 cpatel@elegosoft.com  [IMP] correction,migration,fix unit test errors, (issue#4516)
- 56a39959 2022-03-04 11:37:59 +0100 wagner@elegosoft.com  (feature_4516_blp544_add_files_ported_from_v12_v14) FIXME: comment-out rental procurement run (issue #4516)
- 1453d9de 2022-03-04 11:14:07 +0100 wagner@elegosoft.com  comment out customer-specific trans_purchase_request (issue #4516)
- 774dab78 2022-03-04 10:45:04 +0100 wagner@elegosoft.com  use customer_rank instead of customer for test data (issue #4516)
- bb9f32ed 2022-03-04 00:34:55 +0100 wagner@elegosoft.com  date_expected is gone in stock_move and stock_rule -- still needs fixing (issue #4516)
- f67ef61b 2022-03-03 23:31:30 +0100 wagner@elegosoft.com  odoo-module-migrate -i 12.0 -t 14.0 -d . -m rental_routing -nc (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

