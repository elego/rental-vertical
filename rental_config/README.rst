Rental Config
====================================================

*This file has been generated on 2023-02-19-14-21-34. Changes to it will be overwritten.*

Summary
-------

Rental Config simplifies rental module installation

Description
-----------

Rental Config

This module add some basic configuration options for rental use cases.

Configuration options:
 - Rental Prices: Rental prices can be configured for hourly, daily or monthly rentals.
 - Rental Off-Days: Off-days can be calculated for daily rentals which are excluded from price calculation.
 - Timeline: Use timeline for order regarding a rental product.
 - Rental Product Pack: Rental orders for product packs will also update the stock of pack components.
 - Product Variant: Configure rental products with extended fields and smartbuttons.
 - Product Instance: Use a product as unique product instance with serial number.
 - Product Set: Rental products can be grouped in a set for usage in rental orders.
 - Contract: Rental contracts are automatically created from monthly rentals for periodic invoicing.
 - Repair Order: Support repair orders for product instances.


Usage
-----

Go to Rentals > Configuration > Settings.
Activate the checkboxes for rental extensions.


Changelog
---------

- 9089b1d5 2022-04-15 14:16:12 +0200 wagner@elegosoft.com  (tag: odoo-fox-v15_v15_int_current_daily, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-26, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-25, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-23, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-22, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-21, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-17, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-16, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-15, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-13, tag: daily_odoo-fox-v15_v15_fox_v15_daily_build-12, tag: bp_fox_v15_integration-ceqp-2, tag: bp_fox_v15_integration-cep-27, tag: bp_fox_v15_integration-cep-26, tag: bp_fox_v15_integration-cep-25, tag: bp_fox_v15_integration-cep-23, tag: bp_fox_v15_integration-cep-22, tag: bp_fox_v15_integration-cep-21, tag: bp_fox_v15_integration-cep-17, tag: bp_fox_v15_integration-cep-16, tag: bp_fox_v15_integration-cep-15, tag: bp_fox_v15_integration-cep-13, tag: bp_fox_v15_integration-cep-12, tag: baseline_odoo-fox-v15_v15_fox_v15_daily_build-26, origin/fox_v15_integration-cep-26, origin/fox_v15_integration-cep-25, origin/fox_v15_integration-cep-23, origin/fox_v15_integration-cep-22, origin/fox_v15_integration-cep-21, origin/fox_v15_integration-cep-17, origin/fox_v15_integration-cep-16, origin/fox_v15_integration-cep-15, origin/fox_v15_integration-cep-13, origin/fox_v15_integration-cep-12) update module versions for v15 and remove old migration scripts (issue #4967)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)
