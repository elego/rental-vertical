Rental Product Instance
====================================================

*This file has been generated on 2023-02-19-14-13-59. Changes to it will be overwritten.*

Summary
-------

Add product instances identified by serial number as unique rented objects

Description
-----------

This module extends the product data model in order to mark them as unique product instances 
that are traced by serial number. You might have several instances of a product but they are 
in different conditions or are somehow unique like machines, vehicles or maybe 'used' products.

In order to track the condition history of a product instance you can add operating data, e.g.
you can save the mileage of vehicles or the operating hours of machines.


Usage
-----

- Install the module.
- Create a stockable product.
- Mark the product as product instance.
- Save the product and set an unique serial number.
  Hint: Make an inventory adjustment, if needed.
- Set a product category that can be configured to either use mileage or operating hours as condition.
- Go to the smartbutton for operating data, create the current condition and update it regularly.


Changelog
---------

- 162f44fc 2023-02-17 12:18:02 +0100 wagner@elegosoft.com  (HEAD -> v16, origin/v16, elego-github/v16) automatic porting via odoo-module-migrate -nc -i 15.0 -t 16.0 -d . (issue #4968)
- 9089b1d5 2022-04-15 14:16:12 +0200 wagner@elegosoft.com  (tag: odoo-fox-v15_v15_int_current_daily, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-26, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-25, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-23, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-22, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-21, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-17, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-16, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-15, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-13, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-12, tag: bp_fox_v15_integration-ceqp-2, tag: bp_fox_v15_integration-cep-27, tag: bp_fox_v15_integration-cep-26, tag: bp_fox_v15_integration-cep-25, tag: bp_fox_v15_integration-cep-23, tag: bp_fox_v15_integration-cep-22, tag: bp_fox_v15_integration-cep-21, tag: bp_fox_v15_integration-cep-17, tag: bp_fox_v15_integration-cep-16, tag: bp_fox_v15_integration-cep-15, tag: bp_fox_v15_integration-cep-13, tag: bp_fox_v15_integration-cep-12, tag: baseline_odoo-fox-v15_v15_fox_v15_daily_build-26, origin/fox_v15_integration-cep-26, origin/fox_v15_integration-cep-25, origin/fox_v15_integration-cep-23, origin/fox_v15_integration-cep-22, origin/fox_v15_integration-cep-21, origin/fox_v15_integration-cep-17, origin/fox_v15_integration-cep-16, origin/fox_v15_integration-cep-15, origin/fox_v15_integration-cep-13, origin/fox_v15_integration-cep-12) update module versions for v15 and remove old migration scripts (issue #4967)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 279539a5 2022-03-14 10:48:31 +0100 cpatel@elegosoft.com  [IMP] correction,migration,fix unit test errors, (issue#4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

