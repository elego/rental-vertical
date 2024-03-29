Rental Timeline Product Instance
====================================================

*This file has been generated on 2022-07-26-13-09-49. Changes to it will be overwritten.*

Summary
-------

Extends the rental_timeline module to show the product instance fields in the timeline product popup.

Description
-----------

The rental modules may be used to rent arbitrary products or individual product instances identified by serial number.
In the latter case, product instance-specific information should be displayed in the timeline view, too, which is
added by this module.


Usage
-----

This module is automatically installed when all of the following modules are installed in a database:

- rental_timeline
- rental_product_instance

No further configuration is needed.


Changelog
---------

- 1e549e87 2022-05-04 12:56:56 +0200 wagner@elegosoft.com  (origin/feature_2832_blp7_new_logos_v12, feature_2832_blp7_new_logos_v12) update doc (issue #3613, issue #4016)
- 02eb49c8 2022-05-04 12:18:32 +0200 wagner@elegosoft.com  update doc (issue #4016)
- 4ff94cf3 2022-05-04 12:09:50 +0200 wagner@elegosoft.com  add new rental logo (issue #3613, issue #4016)
- 214cf6a2 2022-04-27 15:13:48 +0200 cpatel@elegosoft.com  (origin/feature_4995_blp1380_refactor_fleet_extensions_v12) [FIX] test errors due to field license_plate and correct remaining ref after refactoring, (issue#4995)
- 1f13e294 2022-04-19 16:47:51 +0200 cpatel@elegosoft.com  [IMP] rental_timeline_product_instance : remove fields related to fleet and vehicle, update translation, (issue#4955)
- 296b6193 2021-10-25 10:20:28 +0200 wagner@elegosoft.com  regenrate documentation (issue #4016)
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- 5fddc156 2021-06-25 15:21:12 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4213_blp1110_timeline_filter_v12: addons-rental-vertical remotes/origin/feature_4213_blp1110_timeline_filter_v12 - cc3f88ac0f704ea56d61229ed238d9590b85f0db [IMP] add new field active for model product.timeline and implements the filter of it.
- 6c3a7802 2021-06-22 20:38:48 +0200 yweng@elegosoft.com  [IMP] improves filter on field product_id for timeline (issue 4214)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- ce643a29 2021-05-20 00:17:54 +0200 yweng@elegosoft.com  (origin/fix_4215_blp1050_timeline_filter_v12) [FIX] product instance timeline
- d4788ddb 2021-02-02 20:04:59 +0100 yweng@elegosoft.com  (origin/feature_3760_blp969_rental_timeline_v12) [IMP] black formatted (issue 3760)
- b92f94f2 2021-02-02 17:36:38 +0100 yweng@elegosoft.com  [IMP] adjust trigger function to update infos in timeline (issue 3760)
- f82eb5d5 2021-02-01 17:07:51 +0100 yweng@elegosoft.com  [IMP] improves performance of timeline (issue 3760)
- a3dbbc3e 2021-01-15 13:20:08 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4041_blp963_filter_instance_state_v12: addons-rental-vertical remotes/origin/feature_4041_blp963_filter_instance_state_v12 - 3d72d4dce46aade56e9ec43c2bad5722c82ccdbc [IMP] add unittest for module rental_timeline_product_instance (issue 4041)
- 3d72d4dc 2021-01-14 17:34:01 +0100 yweng@elegosoft.com  (origin/feature_4041_blp963_filter_instance_state_v12) [IMP] add unittest for module rental_timeline_product_instance (issue 4041)
- 139b5643 2021-01-14 16:04:18 +0100 yweng@elegosoft.com  [IMP] Refactoring of modules rental_product_instance and rental_timeline_product_instance (issue 4041)
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- a35a62d4 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- 408c8282 2020-11-25 10:17:03 +0100 kay.haeusler@elego.de  Fix the constraint for checking for multiple rentals (offers can exist side by side); issue #3722
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 412ee810 2020-10-28 17:11:36 +0100 wagner@elegosoft.com  extend usage for rental_timeline modules (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5c 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5d1c1064 2020-10-28 11:51:40 +0100 wagner@elegosoft.com  add several usage notes for auto-installing modules (issue #3613)
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
- db00762d 2020-03-20 22:42:06 +0100 kay.haeusler@elego.de  formated the fields date_start, date_end, type and product_instance_state; issue #3409
- 4c397d7e 2020-03-20 15:49:09 +0100 kay.haeusler@elego.de  fix the translations; issue #3409
- c4ee80dd 2020-03-19 18:20:08 +0100 kay.haeusler@elego.de  workaround for removing the database ids in the mouse over in the timeline; issue #3591
- b49c01da 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e942 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- e371276d 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- e21ca952 2020-03-09 18:13:39 +0100 kay.haeusler@elego.de  (origin/feature_3409_blp343_rental_timeline_repair_v12) move the constrain _check_date from rental_product_instance to rental_timeline_product_instance; issue #3409
- 804dc443 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771a 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462

