Rental Product Variant
====================================================

*This file has been generated on 2021-06-09-12-38-09. Changes to it will be overwritten.*

Summary
-------

Extends model product with several fields for rental use cases.

Description
-----------

This module adds several fields to the product form.

Additional fields:
 - further_ref [Char]: additional reference
 - qr_code [Char]: QR code
 - manu_year [Char]: year of manufacture
 - manu_id [Many2one]: product.manufacturer -- manufacturer
 - manu_type_id [Many2one]: product.manufacturer.type -- type
 - fleet_type_id [Many2one]: fleet.type -- fleet type

 - rental_order_ids [One2many]: sale.rental -- rented_product_id -- Rental Orders
 - stock_move_ids [One2many]: stock.move -- product_id -- Stock Moves
 - additional_info [Html]: arbitrary additional infomation

Additional fields configured and added by product category:
 - Show Product Identification Number -> product_number [Char]: product identification number
 - Show Vehicle Identification Number -> vehicle_number [Char]: vehicle identification number
 - Show License Plate -> license_plate [Char]: license plate
 - Show Initial Registration -> init_regist [Date]: date of initial registration


Usage
-----

In order to get vehicle related fields, open the product category and activate the desired checkboxes.


Changelog
---------

- 104b890 2021-03-29 13:19:52 +0200 maria.sparenberg@elegosoft.com  (origin/fix_4176_blp1043_sales_smartbutton_v12) issue #4176 fix default argument because otherwise calling this method for sale orders you would need to call it with rental=False
- 7516e2d 2020-11-26 21:13:46 +0100 yweng@elegosoft.com  [IMP] remove some depends of rental_base
- bbd5cb2 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- 98e0d97 2021-01-13 14:59:56 +0100 yweng@elegosoft.com  (origin/feature_4035_blp961_manufacturer_type_v12) [IMP] improve views of manufacturer type (issue 4035)
- a35a62d 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f7 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7e3b59 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2a 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 20bb1bb 2020-10-20 16:23:04 +0200 maria.sparenberg@elegosoft.com  (origin/fix_3783_blp835_remove_style_inline_option_rental_v12) issue #3783 remove option because it might cause the insertion of styles to html texts
- 2f16ca3 2020-10-16 15:46:12 +0200 maria.sparenberg@elegosoft.com  (origin/defect_3873_blp833_html_code_button_v12) issue #3873 show code-view-button in html fields
- 7580ae8 2020-10-05 22:19:25 +0200 wagner@elegosoft.com  (origin/fix_3884_blp819_fix_application_status_and_deps_v12, fix_3884_blp819_fix_application_status_and_deps_v12) set application to false for all modules except rental_base (issue #3884, issue #3339)
- a9d31ee 2020-08-11 16:05:11 +0200 yweng@elegosoft.com  (origin/feature_3765_blp732_rental_product_smartbutton_v12) [IMP] split smartbutton action_view_all_invoice for in invoice and out invoice
- 48b7e28 2020-08-05 12:05:53 +0200 yweng@elegosoft.com  (origin/feature_3816_blp721_quotation_order_menu_v12) [IMP] do not use sale_order_type.normal_sale_type to search the sale.order
- 4153ab5 2020-07-14 22:11:26 +0200 yweng@elegosoft.com  (origin/defect_3765_blp700_product_smartbuttons_v12) [IMP] Adjust smartbutton of product
- d0f0a58 2020-07-10 13:44:37 +0200 cpatel@elegosoft.com  (origin/fix_3765_blp689_rental_product_smartbuttons_count_v12) [FIX] smartbuttons count,Rental,C-Contract,issue#3765
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- f40add6 2020-06-26 10:15:20 +0200 maria.sparenberg@elegosoft.com  (origin/fix_3637_blp666_add_product_identification_number_v12) issue #3637 update German translation and pot-file
- c0f4831 2020-06-26 06:37:53 +0200 wagner@elegosoft.com  (origin/fix_2637_add_product_identification_number_v12, fix_2637_add_product_identification_number_v12) add product_identification_number, show_product_identification_number and change german translation for vehicle number (issue #3637)
- 2619f8f 2020-06-10 17:56:51 +0200 yweng@elegosoft.com  (origin/feature_3668_blp636_set_option_invisible_before_creating_product_v12) [IMP] set translatable for field name of fleet.type
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- af656d0 2020-05-06 17:34:25 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3599_blp543_product_variant_v12) issue #3599 format field definitions and change page string for additional info to specification
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- e5c59af 2020-05-02 00:38:12 +0200 kay.haeusler@elego.de  (origin/feature_3642_blp531_product_highlights_v12) move the menu products from rental_product_variant to rental_base; issue #3642
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- ee4aa16 2020-04-24 18:19:29 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3599_blp488_product_add_info_v12: addons-rental-vertical remotes/origin/feature_3599_blp488_product_add_info_v12 - b89e7ab8e9f73509433b234cbb0af2089feb7eb5 [IMP] active translation of field additional_info
- b89e7ab 2020-04-24 13:05:01 +0200 yweng@elegosoft.com  (origin/feature_3599_blp488_product_add_info_v12) [IMP] active translation of field additional_info
- f0589c7 2020-04-22 10:28:00 +0200 cpatel@elegosoft.com  (origin/feature_3279_blp488_rental_product_todo_points_v12) [IMP] product form changes, issue#3279
- 3db8af4 2020-04-17 18:29:51 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3615_blp461_rental_product_instance_v12: addons-rental-vertical remotes/origin/feature_3615_blp461_rental_product_instance_v12 - d70034acecc018edafc04c561ace080c83a4c86e [FIX] fix dependecy 'purchase_order_type' on rental_product_instance
- f1d5958 2020-04-12 13:54:35 +0200 yweng@elegosoft.com  [ADD] Module shipment_plan, shipment_plan_sale and shipment_plan_rental
- d70034a 2020-04-15 12:22:00 +0200 cpatel@elegosoft.com  (origin/feature_3615_blp461_rental_product_instance_v12) [FIX] fix dependecy 'purchase_order_type' on rental_product_instance
- a91b535 2020-04-15 10:10:33 +0200 cpatel@elegosoft.com  [FIX] fix dependecy 'purchase' on rental_product_instance
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- 94f6f71 2020-03-26 10:09:51 +0100 cpatel@elegosoft.com  [IMP] todo points of rental product , ticket #3279
- 197443e 2020-03-22 16:48:33 +0100 yweng@elegosoft.com  [IMP] improves form-, tree- and search-view of products (issue 3593)
- 3119cfd 2020-03-18 10:07:48 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp384_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp384_extend_documentation_v12 - b49c01dabbc653a42b77f82bd3c44a8759721359 regenerate doc (issue #3339)
- 769b037 2020-03-16 10:28:59 +0100 cpatel@elegosoft.com  (origin/feature_3576_blp384_rental_product_variant_v12) [IMP] improvemets in todo points for ticket #3467,#3279
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 977d224 2020-03-13 10:58:32 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp371_todo_points_v12) [IMP] todo points issue # 3279
- e371276 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- eae607f 2020-03-10 18:13:57 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3279_blp343_todo_points_v12: addons-rental-vertical remotes/origin/feature_3279_blp343_todo_points_v12 - 290795012d9932bfc08060449d3386c2fbcd7483 [IMP] todo points    1. move 'additional info' page behind 'general info' (so it is the second tab)    3. fix the order of smartbuttons       remove 'on hand' smartbutton if product ist product instance       remove 'forecastes' smartbutton if product ist product instance       remove 'routes' smartbutton if product ist product instance       remove 'purchased' smartbutton if product ist product instance       remove 'sold' smartbutton if product ist product instance    4. fix exception after clicking on smartbutton 'sale orders'       ValueError: External ID not found in the system: rental_base.action_normal_orders    5. fix problem that the invoice form view cannot be opend after clicking on smartbutton 'invoices'
- 9576b54 2020-03-09 14:32:43 +0100 wagner@elegosoft.com  (origin/fix_3339_blp343_extend_documentation_v12, fix_3339_blp343_extend_documentation_v12) allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 9ae7b8d 2020-03-09 13:58:15 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3279_blp343_product_config_menu_v12) issue #3279 add submenu for product config in rental menu
- e030fd1 2020-03-09 13:54:52 +0100 maria.sparenberg@elegosoft.com  issue #3279 add description and usage section for rental_product_variant
- 2907950 2020-03-09 10:26:14 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp343_todo_points_v12) [IMP] todo points    1. move 'additional info' page behind 'general info' (so it is the second tab)    3. fix the order of smartbuttons       remove 'on hand' smartbutton if product ist product instance       remove 'forecastes' smartbutton if product ist product instance       remove 'routes' smartbutton if product ist product instance       remove 'purchased' smartbutton if product ist product instance       remove 'sold' smartbutton if product ist product instance    4. fix exception after clicking on smartbutton 'sale orders'       ValueError: External ID not found in the system: rental_base.action_normal_orders    5. fix problem that the invoice form view cannot be opend after clicking on smartbutton 'invoices'
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 4c76ef2 2020-03-04 16:56:16 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp311_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp311_extend_documentation_v12 - 7dde7fa1ec109919795e59198feb24fc96fcfeb1 add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- bf364e7 2020-03-03 19:35:44 +0100 kay.haeusler@elego.de  (origin/feature_3296_blp311_add_fields_to_search_v12) add some fields to the search view; issue #3296
- 7dde7fa 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- 6965ed1 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- 41ec0c4 2020-02-12 17:15:20 +0100 yweng@elegosoft.com  [IMP] redefine fields for instance current condition
- 4d17de4 2020-02-11 16:30:49 +0100 yweng@elegosoft.com  [IMP] adjusts smartbuttons of product variant
- a88dfb5 2020-02-12 12:57:10 +0100 yweng@elegosoft.com  [IMP] refactoring of menus
- d3c07ec 2020-02-11 13:36:17 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3279_blp236_product_instance_German_translation_v12) issue #3279 add German translation for rental_product_variant
- 41fb557 2020-02-07 16:02:55 +0100 yweng@elegosoft.com  [FIX] fixes timeline view errors
- bbcea0f 2020-02-06 15:03:24 +0100 yweng@elegosoft.com  [FIX] fixes error by copying a product variant
- 2f11b55 2020-01-29 17:46:18 +0100 yweng@elegosoft.com  [IMP] improves form view of products
- b5f3dbc 2020-01-23 15:32:23 +0100 yweng@elegosoft.com  [IMP] fixes errors in module rental_product_pack and redefine type of field 'init_regist' Char -> Date
- 94e76bb 2020-01-23 13:08:03 +0100 yweng@elegosoft.com  [IMP] set liscense, copyrights and author
- b2e6d5c 2020-01-21 20:51:21 +0100 yweng@elegosoft.com  (origin/feature_3304_blp151_refactoring_swrent_product_extension_v12) [IMP] Add neu Module rental_base, rental_product_pack and Refactoring of module sale_rental_menu (deprecated)
- 676c70b 2020-01-20 13:40:34 +0100 yweng@elegosoft.com  [IMP] Refactoring of module swrent_product_extension

