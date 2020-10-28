Rental Product Set
====================================================

*This file has been generated on 2020-10-28-20-41-16. Changes to it will be overwritten.*

Summary
-------

Extends the sale_product_set to add rented product set on sale order lines.

Description
-----------

Product sets define a number of products that are frequently sold together and are added
as different sale order lines. This modules extends this use case to renting of product
sets. As in the original workflows, independent rental order lines are created for all
the products in the set. There is no further relation between those products.


Usage
-----

Refer to the usage information of the OCA module sale_product_set to learn how to
define product sets.

This module extends the sale and stock functionality to enable the renting of
OCA product sets. In order to do that, just install the module.

No further configuration is needed.


Changelog
---------

- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  (HEAD -> v12, origin/v12) add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 7580ae8 2020-10-05 22:19:25 +0200 wagner@elegosoft.com  (origin/fix_3884_blp819_fix_application_status_and_deps_v12, fix_3884_blp819_fix_application_status_and_deps_v12) set application to false for all modules except rental_base (issue #3884, issue #3339)
- 114c04c 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- 4d5d64d 2020-07-08 14:11:28 +0200 cpatel@elegosoft.com  (origin/feature_3753_blp689_rental_product_set_v12) [IMP] update unittest for two months ,rental_product_set,issue#3753
- 5ddde45 2020-07-07 15:22:30 +0200 cpatel@elegosoft.com  (origin/feature_3753_blp677_rental_product_set_v12) [IMP] update unit test to rental_product_set module, issue#3753
- 6c6b23c 2020-07-06 14:38:51 +0200 cpatel@elegosoft.com  [IMP] small correction
- b847f3e 2020-07-03 13:50:14 +0200 cpatel@elegosoft.com  [IMP] improves add product set wizard method
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- dccc9aa 2020-03-23 12:15:27 +0100 cpatel@elegosoft.com  (origin/feature_3576_blp400_rental_product_set_unittest_v12) [IMP] unit tests for rental_product_set
- 3119cfd 2020-03-18 10:07:48 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp384_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp384_extend_documentation_v12 - b49c01dabbc653a42b77f82bd3c44a8759721359 regenerate doc (issue #3339)
- a8e3385 2020-03-16 22:30:45 +0100 yweng@elegosoft.com  [IMP] move product_uom_month from rental_pricelist into rental_base
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462
- 7dde7fa 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- 1db4760 2020-02-29 23:48:15 +0100 wagner@elegosoft.com  add some more simple module decsriptions (issue #3339)
- 6965ed1 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- a2502e6 2020-02-11 13:24:27 +0100 maria.sparenberg@elegosoft.com  issue #3279 add German translations for rental_product_set
- 6752ee4 2020-01-23 16:25:00 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp157_rental_product_set_v12) [IMP] set domian on time uom when product set onchnage,add menu Product Set under Rental/Master data
- d44f694 2020-01-23 13:41:14 +0100 yweng@elegosoft.com  [IMP] replace license, copyrights and author for module rental_product_set
- 595188c 2020-01-22 14:00:40 +0100 cpatel@elegosoft.com  [ADD] module rental_product_set added

