Shipment Management Rental
====================================================

*This file has been generated on 2021-10-25-10-18-19. Changes to it will be overwritten.*

Summary
-------

Shipment Management Rental

Description
-----------

This module provides a rental extension for the shipment management.
Rentals require two deliveries, one to transfer the products to the customer and one to get them back.
In case of products that needs special transportation, e.g. because of their weight, height or chemical
properties, two shipment plans are created when requesting transportation from the rental order.


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


Changelog
---------

- dca4ac1b 2021-10-10 18:18:10 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4433_blp1142_rental_base_v12: addons-rental-vertical remotes/origin/feature_4433_blp1142_rental_base_v12 - 75791881da0ea6e70c408ec75042fe9635fc9a49 issue #4433 change view id to match parent id
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- d3cdb63e 2021-09-16 18:39:35 +0200 yweng@elegosoft.com  [IMP] add additional options for wizard create.trans.request and create.sale.trans.request to create single purchase order and single requisition (issue: 4349)
- 61673ce7 2021-07-29 13:19:27 +0200 maria.sparenberg@elegosoft.com  issue #4258 fix test and add description and usage section in manifest
- 39b3c089 2021-07-29 09:53:22 +0200 maria.sparenberg@elegosoft.com  issue #4258 fix rental tests
- 6a1a205e 2021-07-20 15:45:43 +0200 maria.sparenberg@elegosoft.com  issue #4258 refactor and fix translations
- e4dfcb4e 2021-06-29 13:58:57 +0200 yweng@elegosoft.com  [IMP] (issue 4275) improves description of transport and onchange event on sale.order.line. Do not return product for normal sale in a combined order (normal sale + rental)
- 79ad02b9 2021-06-27 12:48:12 +0200 yweng@elegosoft.com  [IMP] adjust Unittest of shipment_plan (issue 4258)
- 7bfba3ef 2021-06-25 15:21:14 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4258_blp1110_shipment_plan_v12: addons-rental-vertical remotes/origin/feature_4258_blp1110_shipment_plan_v12 - a6c718e8bf13718fd1677970d2e9ea097395c610 [IMP] adjust form view of purchase.order and extract function to prepare values for creating pos and prs from shipment plan (issue 4258)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 0c50e185 2021-06-09 03:20:32 +0200 yweng@elegosoft.com  [IMP] improves module shipment_plan shipment_plan_sale shipment_plan_rental and rental_routing (issue 4258)
- 7516e2d5 2020-11-26 21:13:46 +0100 yweng@elegosoft.com  [IMP] remove some depends of rental_base
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7f84e7d 2020-12-09 12:10:15 +0100 yweng@elegosoft.com  (origin/feature_3432_blp906_shipment_plan_unittest_v12) [IMP] Unittest of module shipment_plan_rental
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- 03207593 2020-09-15 10:29:02 +0200 yweng@elegosoft.com  (origin/defect_3602_blp790_duplicated_labels_v12) issue #3602 fix duplicated labels in module shipment_plan_sale and shipment_plan_rental
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 60528429 2020-05-06 20:53:44 +0200 yweng@elegosoft.com  (origin/feature_3432_blp543_forward_shipment_plan_v12) [IMP] use picking type 'internal' for forward transfer and add field 'dangerous_goods' for sale.order.line and shipment.plan
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 09915e6c 2020-04-28 18:32:08 +0200 yweng@elegosoft.com  (origin/feature_3432_blp503_stock_shipment_management_v12) [IMP] improves reference between shipment.plan and stock.picking
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- c1619131 2020-04-17 12:08:33 +0200 yweng@elegosoft.com  [FIX] action_cancel of sale.order
- f1d5958b 2020-04-12 13:54:35 +0200 yweng@elegosoft.com  [ADD] Module shipment_plan, shipment_plan_sale and shipment_plan_rental

