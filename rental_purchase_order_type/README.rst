Rental Purchase Order Type
====================================================

*This file has been generated on 2023-02-19-14-13-59. Changes to it will be overwritten.*

Summary
-------

Additional purchase order types for rental use cases: transport orders and repair orders

Description
-----------

This module provides the possibility to distiguish purchase orders by the type 'transport' and 'repair' orders', 
using the module purchase_order_type. It also adds new menu entries for transport and repair vendor (purchase) 
orders in the rental application.

Additional order types:
 - Transport Order: used to order transportation for rented products via vehicle, ship or airplane
 - Repair Order: used to order repair work during rental periods


Usage
-----

- Install the module.
- Create a purchase order as a transport order here: Rental > Vendors > Transport Order.
- Create a purchase order as a repair order here: Rental > Vendors > Repair Order.
- Create a purchase order and set manually the purchase order type as desired.


Changelog
---------

- 162f44fc 2023-02-17 12:18:02 +0100 wagner@elegosoft.com  (HEAD -> v16, origin/v16, elego-github/v16) automatic porting via odoo-module-migrate -nc -i 15.0 -t 16.0 -d . (issue #4968)
- 9089b1d5 2022-04-15 14:16:12 +0200 wagner@elegosoft.com  (tag: odoo-fox-v15_v15_int_current_daily, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-26, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-25, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-23, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-22, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-21, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-17, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-16, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-15, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-13, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-12, tag: bp_fox_v15_integration-ceqp-2, tag: bp_fox_v15_integration-cep-27, tag: bp_fox_v15_integration-cep-26, tag: bp_fox_v15_integration-cep-25, tag: bp_fox_v15_integration-cep-23, tag: bp_fox_v15_integration-cep-22, tag: bp_fox_v15_integration-cep-21, tag: bp_fox_v15_integration-cep-17, tag: bp_fox_v15_integration-cep-16, tag: bp_fox_v15_integration-cep-15, tag: bp_fox_v15_integration-cep-13, tag: bp_fox_v15_integration-cep-12, tag: baseline_odoo-fox-v15_v15_fox_v15_daily_build-26, origin/fox_v15_integration-cep-26, origin/fox_v15_integration-cep-25, origin/fox_v15_integration-cep-23, origin/fox_v15_integration-cep-22, origin/fox_v15_integration-cep-21, origin/fox_v15_integration-cep-17, origin/fox_v15_integration-cep-16, origin/fox_v15_integration-cep-15, origin/fox_v15_integration-cep-13, origin/fox_v15_integration-cep-12) update module versions for v15 and remove old migration scripts (issue #4967)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

