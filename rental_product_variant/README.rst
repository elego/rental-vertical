Rental Product Variant
====================================================

*This file has been generated on 2022-04-10-15-34-31. Changes to it will be overwritten.*

Summary
-------

Extends model product with several fields for rental use cases.

Description
-----------

This module adds several fields to the product form.

Additional fields:
 - further_ref [Char]: additional reference
 - qr_code [Char]: QR code
 - manu_year [Char]: year of manufacture
 - manu_id [Many2one]: product.manufacturer -- manufacturer
 - manu_type_id [Many2one]: product.manufacturer.type -- type
 - fleet_type_id [Many2one]: fleet.type -- fleet type

 - rental_order_ids [One2many]: sale.rental -- rented_product_id -- Rental Orders
 - stock_move_ids [One2many]: stock.move -- product_id -- Stock Moves
 - additional_info [Html]: arbitrary additional infomation

Additional fields configured and added by product category:
 - Show Product Identification Number -> product_number [Char]: product identification number
 - Show Vehicle Identification Number -> vehicle_number [Char]: vehicle identification number
 - Show License Plate -> license_plate [Char]: license plate
 - Show Initial Registration -> init_regist [Date]: date of initial registration


Usage
-----

In order to get vehicle related fields, open the product category and activate the desired checkboxes.


Changelog
---------

- ac980b89 2022-02-28 17:36:28 +0100 cpatel@elegosoft.com  [FIX][IMP] correct code, (issue#4516)
- 5780031a 2022-02-23 22:22:08 +0100 wagner@elegosoft.com  try to resolve unresolved conflicts from mass merge (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

