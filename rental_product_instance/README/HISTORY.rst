
Changelog
---------

- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 977d224 2020-03-13 10:58:32 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp371_todo_points_v12) [IMP] todo points issue # 3279
- 705a197 2020-03-12 23:49:11 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3576_blp355_rental_product_pack_v12: addons-rental-vertical remotes/origin/feature_3576_blp355_rental_product_pack_v12 - b367d1778430938c768f5ab84bd8e543f34f113f [IMP] Unittests of module rental_product_instance
- b367d17 2020-03-11 22:02:43 +0100 yweng@elegosoft.com  (origin/feature_3576_blp355_rental_product_pack_v12) [IMP] Unittests of module rental_product_instance
- a0aa278 2020-03-11 18:13:01 +0100 kay.haeusler@elego.de  (origin/feature_3477_blp355_rental_product_instance_v12) code formating; issue #3477
- e371276 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- c42b63f 2020-03-10 18:14:00 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3409_blp343_rental_timeline_repair_v12: addons-rental-vertical remotes/origin/feature_3409_blp343_rental_timeline_repair_v12 - e21ca952a0db68ffd537b070f1d516f1c0fb50ba move the constrain _check_date from rental_product_instance to rental_timeline_product_instance; issue #3409
- e21ca95 2020-03-09 18:13:39 +0100 kay.haeusler@elego.de  (origin/feature_3409_blp343_rental_timeline_repair_v12) move the constrain _check_date from rental_product_instance to rental_timeline_product_instance; issue #3409
- 2907950 2020-03-09 10:26:14 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp343_todo_points_v12) [IMP] todo points    1. move 'additional info' page behind 'general info' (so it is the second tab)    3. fix the order of smartbuttons       remove 'on hand' smartbutton if product ist product instance       remove 'forecastes' smartbutton if product ist product instance       remove 'routes' smartbutton if product ist product instance       remove 'purchased' smartbutton if product ist product instance       remove 'sold' smartbutton if product ist product instance    4. fix exception after clicking on smartbutton 'sale orders'       ValueError: External ID not found in the system: rental_base.action_normal_orders    5. fix problem that the invoice form view cannot be opend after clicking on smartbutton 'invoices'
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462
- 4c76ef2 2020-03-04 16:56:16 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp311_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp311_extend_documentation_v12 - 7dde7fa1ec109919795e59198feb24fc96fcfeb1 add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- bf364e7 2020-03-03 19:35:44 +0100 kay.haeusler@elego.de  (origin/feature_3296_blp311_add_fields_to_search_v12) add some fields to the search view; issue #3296
- 7dde7fa 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- ec77333 2020-03-01 00:11:54 +0100 wagner@elegosoft.com  fix some minor mistakes (issue #3339)
- 1db4760 2020-02-29 23:48:15 +0100 wagner@elegosoft.com  add some more simple module decsriptions (issue #3339)
- 6965ed1 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- b314b6c 2020-02-27 23:00:29 +0100 kay.haeusler@elego.de  show repair and transport orders in the timeline view; issue #3409
- 41ec0c4 2020-02-12 17:15:20 +0100 yweng@elegosoft.com  [IMP] redefine fields for instance current condition
- 5e271b8 2020-02-11 13:01:07 +0100 maria.sparenberg@elegosoft.com  issue #3279 add German translations for rental_product_instance
- 2f11b55 2020-01-29 17:46:18 +0100 yweng@elegosoft.com  [IMP] improves form view of products
- b42fa76 2020-01-28 17:08:41 +0100 yweng@elegosoft.com  [IMP] add some product instance special fields
- 94e76bb 2020-01-23 13:08:03 +0100 yweng@elegosoft.com  [IMP] set liscense, copyrights and author
- b2e6d5c 2020-01-21 20:51:21 +0100 yweng@elegosoft.com  (origin/feature_3304_blp151_refactoring_swrent_product_extension_v12) [IMP] Add neu Module rental_base, rental_product_pack and Refactoring of module sale_rental_menu (deprecated)
- 676c70b 2020-01-20 13:40:34 +0100 yweng@elegosoft.com  [IMP] Refactoring of module swrent_product_extension

