Rental Timeline
====================================================

*This file has been generated on 2020-10-28-17-07-37. Changes to it will be overwritten.*

Summary
-------

Adds a timeline to products as well as a timeline view as overview of all rental products and orders

Description
-----------

This module extends the rental_sale module to create and change the timeline objects
for the rented product instances automatically.
A complete timeline view containing all rental orders will be generated for all rentable products.

This module adds the basic rental timeline view as well as an extension to the product form view.


Usage
-----

Just install this module to add the rental timeline view to your system. No further configuration is necessary.


Changelog
---------

- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  (HEAD -> v12, origin/v12) change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- adcc40f 2020-10-07 10:19:08 +0200 maria.sparenberg@elegosoft.com  (origin/defect_3878_blp824_update_times_v12) issue #3878 fix arguments for update times because start date was also written as end date
- b7dad08 2020-10-06 13:48:11 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3884_blp819_fix_application_status_and_deps_v12: addons-rental-vertical remotes/origin/fix_3884_blp819_fix_application_status_and_deps_v12 - 7580ae8936652f96fb11ac212867967458a4e127 set application to false for all modules except rental_base (issue #3884, issue #3339)
- 7580ae8 2020-10-05 22:19:25 +0200 wagner@elegosoft.com  (origin/fix_3884_blp819_fix_application_status_and_deps_v12, fix_3884_blp819_fix_application_status_and_deps_v12) set application to false for all modules except rental_base (issue #3884, issue #3339)
- b4743f7 2020-10-05 16:13:02 +0200 maria.sparenberg@elegosoft.com  (origin/defect_3880_blp819_timeline_confirmed_so_v12) issue #3880 allow updating confirmed order lines and corresponding timeline entries and contract lines
- 79d9f43 2020-10-02 14:02:24 +0200 maria.sparenberg@elegosoft.com  issue #3880 create timeline object for sale order lines in state 'sale'
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 8cc4c7a 2020-09-08 13:11:20 +0200 kay.haeusler@elego.de  (origin/defect_3863_blp776_recreating_timeline_items_v12) recreating the timeline items when the order is setting from cancel to draft; issue #3863
- a196d00 2020-07-13 09:22:09 +0200 yweng@elegosoft.com  (origin/feature_3760_blp695_rental_menu_dashboard_v12) [IMP] add menu dashboard
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- e52be41 2020-06-24 12:33:36 +0200 yweng@elegosoft.com  (origin/defect_3729_blp662_sell_service_in_rental_order_v12) [IMP] adjust function _get_product_domain to sell normal service in rental order (issue 3729)
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 5a1a6dc 2020-05-06 09:52:48 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3409_blp543_rental_timeline_colors_v12) issue #3409 change color in timeline view
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- b081ed1 2020-04-08 18:49:30 +0200 ycervantes@elegosoft.com  (origin/fix_3623_blp435_web_timeline_extend_v12) [ADD] custom view_type named rental_timeline
- 1430ab8 2020-04-07 12:14:14 +0200 ycervantes@elegosoft.com  [FIX] use extend instead of include in TimelineRenderer
- b0d605b 2020-03-30 16:42:43 +0200 kay.haeusler@elego.de  (origin/feature_3409_blp420_rental_timeline_v12) remove the product_instance condition; issue #3409
- 3efeb14 2020-03-24 17:40:06 +0100 kay.haeusler@elego.de  (origin/feature_3409_blp412_rental_timeline_v12) unlink also the entries in product.timeline if the main object is unlink; issue #3409
- 5533e36 2020-03-22 21:48:23 +0100 kay.haeusler@elego.de  (origin/feature_3409_blp400_rental_timeline_v12) open the dialogs in readonly mode; issue #3409
- db00762 2020-03-20 22:42:06 +0100 kay.haeusler@elego.de  formated the fields date_start, date_end, type and product_instance_state; issue #3409
- 4c397d7 2020-03-20 15:49:09 +0100 kay.haeusler@elego.de  fix the translations; issue #3409
- 036a10e 2020-03-22 21:49:14 +0100 kay.haeusler@elego.de  remove unnecessary logger outputs; issue #3409
- c4ee80d 2020-03-19 18:20:08 +0100 kay.haeusler@elego.de  workaround for removing the database ids in the mouse over in the timeline; issue #3591
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 1d4b0b9 2020-03-11 21:29:48 +0100 kay.haeusler@elego.de  (origin/feature_3409_blp355_rental_timeline_v12) adjust the start point on clicking the scale buttons; issue #3409
- f3ea64f 2020-03-11 21:28:40 +0100 kay.haeusler@elego.de  fix the order_name; issue #3409
- e371276 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 5fc8c62 2020-03-08 18:26:39 +0100 kay.haeusler@elego.de  outsource the displaying of the icons to two separate modules; issue #3409
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462
