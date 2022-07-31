Rental Purchase Order Type
====================================================

*This file has been generated on 2022-07-26-13-09-49. Changes to it will be overwritten.*

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

- 1e549e87 2022-05-04 12:56:56 +0200 wagner@elegosoft.com  (origin/feature_2832_blp7_new_logos_v12, feature_2832_blp7_new_logos_v12) update doc (issue #3613, issue #4016)
- 02eb49c8 2022-05-04 12:18:32 +0200 wagner@elegosoft.com  update doc (issue #4016)
- 4ff94cf3 2022-05-04 12:09:50 +0200 wagner@elegosoft.com  add new rental logo (issue #3613, issue #4016)
- 296b6193 2021-10-25 10:20:28 +0200 wagner@elegosoft.com  regenrate documentation (issue #4016)
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 7516e2d5 2020-11-26 21:13:46 +0100 yweng@elegosoft.com  [IMP] remove some depends of rental_base
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5c 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 86e7c1a6 2020-10-28 12:35:56 +0100 maria.sparenberg@elegosoft.com  issue #3613 add manifest description and usage for several rental modules
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d8 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932a 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340dc 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b3 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d2 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- b49c01da 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e942 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 804dc443 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 7dde7fa1 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- c63a6d1c 2020-03-01 14:54:55 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3491_blp297_rental_purchase_order_type_v12: addons-rental-vertical remotes/origin/feature_3491_blp297_rental_purchase_order_type_v12 - 08b47a26c62ea472dbf53e0b3f415eea6925bc04 add sequences for the purchase order types 'Transport Order' and 'Repair Order'; issue #3491
- 467665c9 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- 1db47608 2020-02-29 23:48:15 +0100 wagner@elegosoft.com  add some more simple module decsriptions (issue #3339)
- 6965ed1c 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- 08b47a26 2020-02-26 18:50:15 +0100 kay.haeusler@elego.de  (origin/feature_3491_blp297_rental_purchase_order_type_v12) add sequences for the purchase order types 'Transport Order' and 'Repair Order'; issue #3491
- 690c4d9c 2020-02-23 20:49:28 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp256_rental_vertical_menus_v12) add the addon rental_purchase_order_type; issue #3462

