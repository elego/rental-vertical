Rental Quality Control
====================================================

*This file has been generated on 2021-01-14-13-44-51. Changes to it will be overwritten.*

Summary
-------

New text field to define the reason for quality failure.

Description
-----------

This module extends the quality_control_stock module to add a reason
for failure during quality control, Inspections count smart button on Product form view
and two Quality Control menus under Rental/Customers/Delivery for Customers and
Rental/Vendor/Delivery for the Vendors.


Usage
-----

- Install the module.
- During the quality control workflow,you can define reason for failure in inspection line.
- You can see Inspections count on Product.
- You can see two Quality Control menus under Rental/Customers/Delivery for Customers and
  Rental/Vendor/Delivery for the Vendors.

Changelog
---------

- a35a62d 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f7 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7e3b59 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 8281e1a 2020-11-05 11:28:32 +0100 cpatel@elegosoft.com  [IMP] add missing usage details,rental_quality_control
- 391ef2a 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 7580ae8 2020-10-05 22:19:25 +0200 wagner@elegosoft.com  (origin/fix_3884_blp819_fix_application_status_and_deps_v12, fix_3884_blp819_fix_application_status_and_deps_v12) set application to false for all modules except rental_base (issue #3884, issue #3339)
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 396490e 2020-05-16 13:18:00 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp559_refactor_menu_view_v12: addons-rental-vertical remotes/origin/fix_3339_blp559_refactor_menu_view_v12 - 89adaaf36d7d2e9e16214501d4ad516a1eb7a007 fixup categories and regenerate documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 09a3564 2020-05-11 18:38:34 +0200 cpatel@elegosoft.com  [IMP] rental tour : 4. return of a rented product including quality control, issue#3615
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 37e24aa 2020-03-12 09:02:35 +0100 cpatel@elegosoft.com  (origin/feature_3576_blp355_rental_quality_control_v12) [IMP] code standard using flake8
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 7dde7fa 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- 6965ed1 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- 50d383a 2020-02-19 14:59:04 +0100 kay.haeusler@elego.de  reorder and create new rental menu items; issue #3462
- 7e34d11 2020-02-11 13:48:13 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3298_blp236_quality_german_translation_v12) issue #3298 add German translations
- 489a4fd 2020-01-29 15:01:14 +0100 cpatel@elegosoft.com  [IMP] add Inspection smart button on product form, add modules in res.config.settings of rental_base
- c8173a9 2020-01-23 16:46:42 +0100 cpatel@elegosoft.com  (origin/feature_3298_blp157_rental_quality_control_v12) [ADD] rental_quality_control module added

