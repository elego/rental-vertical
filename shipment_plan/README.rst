Shipment Management
====================================================

*This file has been generated on 2021-10-25-10-18-19. Changes to it will be overwritten.*

Summary
-------

Shipment Management

Description
-----------

This module provides the base of the shipment management in order to organize and manage transportation
for products that are to voluminous or heavy or somehow dangerous, and therefore need special transport treatment.
The shipment plans focus on the transport after leaving or before entering the internal stock locations.


Usage
-----

Configure the storable products that need transportation.
 - Set the product type to 'Storable Product'.
 - Set the flag 'Transport required' (trans_purchase_request) to True.

Configure transport services that can be purchased from delivery carriers.
 - Set the product type to 'Service'.
 - Set the flag 'Transport Service' (is_transport) to True.
 - Go to Page 'Purchase' amd add some suppliers that offer this transport service.
 - Also choose the 'Transport Service Type' in order to create a purchase order or a call for tender.

Configure the granularity of transport costs.
 - Go to Inventory > Configuration > Settings
 - Choose the transport cost type as single or multiple positions.

 Choosing the cost type 'Multi Positions’ the transport purchase order or call for tender can contain several lines
 for the different costs related to the transport, e.g. the transport costs itself and several charges.
 You can define the appropriate transport services when creating a new transport request.
 Choosing the cost type 'Single Position’ the transport request will only consist of one line with all costs.

Create a new shipment plan and purchase requests.
 - Go to Inventory > Operation > Shipment Plans.
 - Choose the starting address and the destination address.
 - Set the estimated time or arrival and departure.
 - Give some more description that the transport carrier will need.
 - Create a new purchase request by button click.
 - Choose the transport service.
 - Choose the request type to be either a purchase order or requisition (tender).
 - Create a purchase order or requistion.
 - Use these purchase orders as usual.

 Create a shipment plan for internal pickings.
  - Go to Inventory > Configuration > Settings and activate multiple storage locations.
  - Go to Inventory > Operation > Transfers.
  - Create a new stock picking with internal picking type.
  - Create a shipment plan for this internal transfer, which is then linked in a smartbutton.


Changelog
---------

- ce77a323 2021-10-25 10:17:16 +0200 wagner@elegosoft.com  (HEAD -> v12) fix two syntax errors in documentation (issue #3339)
- 996b4742 2021-10-25 10:15:33 +0200 wagner@elegosoft.com  fix two syntax errors in documentation (issue #3339)
- dca4ac1b 2021-10-10 18:18:10 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4433_blp1142_rental_base_v12: addons-rental-vertical remotes/origin/feature_4433_blp1142_rental_base_v12 - 75791881da0ea6e70c408ec75042fe9635fc9a49 issue #4433 change view id to match parent id
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- 8d9bae9c 2021-09-16 19:14:49 +0200 yweng@elegosoft.com  (origin/feature_4258_blp1142_shipment_plan_v12) [IMP] Update translations for module shipment_plan and shipment_plan_sale
- d3cdb63e 2021-09-16 18:39:35 +0200 yweng@elegosoft.com  [IMP] add additional options for wizard create.trans.request and create.sale.trans.request to create single purchase order and single requisition (issue: 4349)
- f67f4850 2021-09-13 15:27:09 +0200 yweng@elegosoft.com  [IMP] add fields location_id and location_dest_id for shipment.plan (issue 4353)
- 78c008d1 2021-07-29 12:17:32 +0200 maria.sparenberg@elegosoft.com  issue #4258 some more refactoring - move stock stuff from shipment_plan_sale to shipment_plan
- 121d6139 2021-07-27 15:59:36 +0200 maria.sparenberg@elegosoft.com  issue #4258 refactor, fix dependencies and add description and usage section in manifest
- 44e04995 2021-07-26 15:45:26 +0200 maria.sparenberg@elegosoft.com  issue #4258 add shipment plan smartbutton in purchase orders
- 6a1a205e 2021-07-20 15:45:43 +0200 maria.sparenberg@elegosoft.com  issue #4258 refactor and fix translations
- 5df1a414 2021-06-29 17:07:31 +0200 yweng@elegosoft.com  [FIX] rental_forward_shipment_plan (issue 4255)
- 79ad02b9 2021-06-27 12:48:12 +0200 yweng@elegosoft.com  [IMP] adjust Unittest of shipment_plan (issue 4258)
- 7bfba3ef 2021-06-25 15:21:14 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4258_blp1110_shipment_plan_v12: addons-rental-vertical remotes/origin/feature_4258_blp1110_shipment_plan_v12 - a6c718e8bf13718fd1677970d2e9ea097395c610 [IMP] adjust form view of purchase.order and extract function to prepare values for creating pos and prs from shipment plan (issue 4258)
- a6c718e8 2021-06-17 17:47:03 +0200 yweng@elegosoft.com  (origin/feature_4258_blp1110_shipment_plan_v12) [IMP] adjust form view of purchase.order and extract function to prepare values for creating pos and prs from shipment plan (issue 4258)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 0c50e185 2021-06-09 03:20:32 +0200 yweng@elegosoft.com  [IMP] improves module shipment_plan shipment_plan_sale shipment_plan_rental and rental_routing (issue 4258)
- 965b09db 2021-05-27 23:13:35 +0200 yweng@elegosoft.com  (origin/fix_4257_blp1102_shipment_plan_v12) [FIX] function create_purchase_request (issue 4257)
- d1c5b3d1 2021-01-22 18:40:01 +0100 wagner@elegosoft.com  (origin/fix_3756_blp492_rental_tours_v12, fix_3756_blp492_rental_tours_v12) add dependency from shipment_plan to rental_base (issue #3756)
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7f84e7d 2020-12-09 12:10:15 +0100 yweng@elegosoft.com  (origin/feature_3432_blp906_shipment_plan_unittest_v12) [IMP] Unittest of module shipment_plan_rental
- 075d2a0d 2020-12-08 22:16:17 +0100 yweng@elegosoft.com  [IMP] Unittest of module shipment_plan_sale
- 32041af5 2020-12-08 22:15:37 +0100 yweng@elegosoft.com  [FIX] add some depends on functions of computed fields in module shipment_plan and shipment_plan_sale
- ea3f3d4d 2020-12-07 23:00:07 +0100 yweng@elegosoft.com  [IMP] Unittests of module shipment_plan
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 60528429 2020-05-06 20:53:44 +0200 yweng@elegosoft.com  (origin/feature_3432_blp543_forward_shipment_plan_v12) [IMP] use picking type 'internal' for forward transfer and add field 'dangerous_goods' for sale.order.line and shipment.plan
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- a2187ec2 2020-04-17 18:26:43 +0200 yweng@elegosoft.com  (origin/feature_3293_blp461_shipment_plan_v12) [IMP] improves UIs for feature shipment_plan
- c1619131 2020-04-17 12:08:33 +0200 yweng@elegosoft.com  [FIX] action_cancel of sale.order
- f1d5958b 2020-04-12 13:54:35 +0200 yweng@elegosoft.com  [ADD] Module shipment_plan, shipment_plan_sale and shipment_plan_rental

