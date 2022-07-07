Shipment Management Sale
====================================================

*This file has been generated on 2022-05-04-12-55-06. Changes to it will be overwritten.*

Summary
-------

Shipment Management Sale

Description
-----------

This module provides a sale extension for the shipment management.
The combination of a storable product that needs transportation and the use of an incoterm configured for outbound
transportation allows the salesmen to create a transport request (purchase order or requisition) directly from the
sale order. It will also create the shipment plan.


Usage
-----

Configure storable and service products as described in module 'shipment_plan'.

Configure incoterms that should allow the creation of transport requests from sale orders.
 - Go to Invoicing > Configuration > Incoterms
 - Set the field 'Outbound transport required' (trans_pr_needed) to True.

Create a sale order for a product that needs transportation.
 - Go to Sales > Orders > Quotations.
 - Create a new quotation.
 - Choose a customer.
 - Choose an incoterm configured to allow the creation of a transport request.
 - Add a storable product that needs transportation.
 - Save the order.
 - Click the button 'Request Transport'.
 - Choose the transport service that should be used in the purchase order / requisition.
 - Create the request.
 - Check the shipment plan, purchase requisition and/or purchase orders.


Changelog
---------

- a035624c 2021-11-26 17:49:24 +0100 yweng@elegosoft.com  (origin/feature_4353_blp1290_shipment_plan_v12) [IMP] extract function _prepare_cost_line() from action_create_trans_cost() of sale.order (issue 4553)
- fb728eef 2021-11-26 17:07:06 +0100 yweng@elegosoft.com  [IMP] improves wizard create.sale.trans.request (issue 4353)
- 131292b3 2021-11-22 12:32:15 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4349_blp1268_shipment_plan_v12: addons-rental-vertical remotes/origin/feature_4349_blp1268_shipment_plan_v12 - 7d6ce349c66ef7eb68bea5c612f2428ab93abb4d [FIX] singleton error (issue 4561)
- 5b3b3302 2021-11-16 12:59:13 +0100 yweng@elegosoft.com  [IMP] add option required for field partner_id of create.transport.request and create.sale.transport.request (issue 4349)
- 830d8fa6 2021-11-05 13:35:28 +0100 wagner@elegosoft.com  Revert "fix: add missing noupdate for shipment settings (issue #3339)"
- 4086b646 2021-11-05 13:35:16 +0100 wagner@elegosoft.com  Revert "fix syntax for shipment settings (issue #3339)"
- a60b7214 2021-11-05 13:05:49 +0100 wagner@elegosoft.com  fix syntax for shipment settings (issue #3339)
- 22e4d7b5 2021-11-05 12:22:34 +0100 wagner@elegosoft.com  Merge remote-tracking branch 'origin/fix_4258_blp1268_shipment_plan_v12' into v12
- 0461a604 2021-11-05 12:20:14 +0100 wagner@elegosoft.com  fix: add missing noupdate for shipment settings (issue #3339)
- 6466c3f4 2021-11-05 12:18:42 +0100 yweng@elegosoft.com  (origin/fix_4258_blp1268_shipment_plan_v12) [FIX] add noupdate=1 for auto res_config_settings
- 842e4978 2021-11-04 19:18:28 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4349_blp1254_shipment_plan_v12: addons-rental-vertical remotes/origin/feature_4349_blp1254_shipment_plan_v12 - 18939f75589e41bcae95ed51ddc7be729dd9fdaa [IMP] add option required for field 'multi' of create.transport.request (issue 4349)
- 18939f75 2021-11-04 13:38:26 +0100 yweng@elegosoft.com  (origin/feature_4349_blp1254_shipment_plan_v12) [IMP] add option required for field 'multi' of create.transport.request (issue 4349)
- 296b6193 2021-10-25 10:20:28 +0200 wagner@elegosoft.com  regenrate documentation (issue #4016)
- dca4ac1b 2021-10-10 18:18:10 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4433_blp1142_rental_base_v12: addons-rental-vertical remotes/origin/feature_4433_blp1142_rental_base_v12 - 75791881da0ea6e70c408ec75042fe9635fc9a49 issue #4433 change view id to match parent id
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- 8d9bae9c 2021-09-16 19:14:49 +0200 yweng@elegosoft.com  (origin/feature_4258_blp1142_shipment_plan_v12) [IMP] Update translations for module shipment_plan and shipment_plan_sale
- d3cdb63e 2021-09-16 18:39:35 +0200 yweng@elegosoft.com  [IMP] add additional options for wizard create.trans.request and create.sale.trans.request to create single purchase order and single requisition (issue: 4349)
- 78c008d1 2021-07-29 12:17:32 +0200 maria.sparenberg@elegosoft.com  issue #4258 some more refactoring - move stock stuff from shipment_plan_sale to shipment_plan
- 121d6139 2021-07-27 15:59:36 +0200 maria.sparenberg@elegosoft.com  issue #4258 refactor, fix dependencies and add description and usage section in manifest
- 6a1a205e 2021-07-20 15:45:43 +0200 maria.sparenberg@elegosoft.com  issue #4258 refactor and fix translations
- 79ad02b9 2021-06-27 12:48:12 +0200 yweng@elegosoft.com  [IMP] adjust Unittest of shipment_plan (issue 4258)
- 7bfba3ef 2021-06-25 15:21:14 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4258_blp1110_shipment_plan_v12: addons-rental-vertical remotes/origin/feature_4258_blp1110_shipment_plan_v12 - a6c718e8bf13718fd1677970d2e9ea097395c610 [IMP] adjust form view of purchase.order and extract function to prepare values for creating pos and prs from shipment plan (issue 4258)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 0c50e185 2021-06-09 03:20:32 +0200 yweng@elegosoft.com  [IMP] improves module shipment_plan shipment_plan_sale shipment_plan_rental and rental_routing (issue 4258)
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7f84e7d 2020-12-09 12:10:15 +0100 yweng@elegosoft.com  (origin/feature_3432_blp906_shipment_plan_unittest_v12) [IMP] Unittest of module shipment_plan_rental
- 7f11ac7a 2020-12-09 12:08:56 +0100 yweng@elegosoft.com  [ADD] auto settings for module shipment_plan_sale
- 075d2a0d 2020-12-08 22:16:17 +0100 yweng@elegosoft.com  [IMP] Unittest of module shipment_plan_sale
- 32041af5 2020-12-08 22:15:37 +0100 yweng@elegosoft.com  [FIX] add some depends on functions of computed fields in module shipment_plan and shipment_plan_sale
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- 03207593 2020-09-15 10:29:02 +0200 yweng@elegosoft.com  (origin/defect_3602_blp790_duplicated_labels_v12) issue #3602 fix duplicated labels in module shipment_plan_sale and shipment_plan_rental
- 471f5401 2020-06-30 20:31:19 +0200 yweng@elegosoft.com  (origin/feature_3293_blp677_internal_picking_shipment_plan_v12) [IMP] create shipment plan from internal stock picking
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 60528429 2020-05-06 20:53:44 +0200 yweng@elegosoft.com  (origin/feature_3432_blp543_forward_shipment_plan_v12) [IMP] use picking type 'internal' for forward transfer and add field 'dangerous_goods' for sale.order.line and shipment.plan
- 817bca78 2020-05-06 15:16:39 +0200 yweng@elegosoft.com  [FIX] view of sale.order to show the button of shipment.plan
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- fbdac576 2020-04-29 20:43:38 +0200 yweng@elegosoft.com  (origin/feature_3432_blp521_stock_shipment_plan_v12) [IMP] set invisible for field trans_pr_needed of sale.order.line
- 09915e6c 2020-04-28 18:32:08 +0200 yweng@elegosoft.com  (origin/feature_3432_blp503_stock_shipment_management_v12) [IMP] improves reference between shipment.plan and stock.picking
- b7dcb59a 2020-04-24 21:00:25 +0200 yweng@elegosoft.com  [IMP] Relation between shipment.plan and stock.picking
- 468bac35 2020-04-28 17:56:41 +0200 yweng@elegosoft.com  [IMP] Calculate Transport Sales Margin as percent number
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- a2187ec2 2020-04-17 18:26:43 +0200 yweng@elegosoft.com  (origin/feature_3293_blp461_shipment_plan_v12) [IMP] improves UIs for feature shipment_plan
- c1619131 2020-04-17 12:08:33 +0200 yweng@elegosoft.com  [FIX] action_cancel of sale.order
- f1d5958b 2020-04-12 13:54:35 +0200 yweng@elegosoft.com  [ADD] Module shipment_plan, shipment_plan_sale and shipment_plan_rental

