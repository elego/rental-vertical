Rental Product Variant Fleet
====================================================

*This file has been generated on 2022-05-04-12-55-06. Changes to it will be overwritten.*

Summary
-------

Extends model product with fields,related to fleet and vehicle specific.

Description
-----------

This module adds several fields to the product form.

Additional fields:
 - fleet_type_id [Many2one]: fleet.type -- fleet type

Additional fields configured and added by product category:
 - Show Vehicle Identification Number -> vehicle_number [Char]: vehicle identification number
 - Show License Plate -> license_plate [Char]: license plate
 - Show Initial Registration -> init_regist [Date]: date of initial registration


Usage
-----

In order to get vehicle related fields, open the product category and activate the desired checkboxes.


Changelog
---------

- eee26e11 2022-05-04 12:20:20 +0200 wagner@elegosoft.com  (HEAD -> feature_2832_blp7_new_logos_v12, origin/feature_2832_blp7_new_logos_v12) add missing README.rst files (issue #4016)
- 02eb49c8 2022-05-04 12:18:32 +0200 wagner@elegosoft.com  update doc (issue #4016)
- 4ff94cf3 2022-05-04 12:09:50 +0200 wagner@elegosoft.com  add new rental logo (issue #3613, issue #4016)
- 214cf6a2 2022-04-27 15:13:48 +0200 cpatel@elegosoft.com  (origin/feature_4995_blp1380_refactor_fleet_extensions_v12) [FIX] test errors due to field license_plate and correct remaining ref after refactoring, (issue#4995)
- e7f1fd54 2022-04-19 17:05:12 +0200 cpatel@elegosoft.com  [IMP] rental_timeline_product_instance_maintenance : add translation files, small changes(issue#4955)
- 4ec18d57 2022-04-19 16:40:32 +0200 cpatel@elegosoft.com  [IMP] rental_product_variant_fleet : add translation files, (issue#4955)
- 1730e660 2022-04-14 15:09:43 +0200 cpatel@elegosoft.com  (origin/feature_4995_blp1379_refactor_fleet_extensions_v12) [IMP] refactore fleet and vehicle related fields,(issue#4955)

