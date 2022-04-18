Rental Contract Insurance
====================================================

*This file has been generated on 2021-10-25-10-18-19. Changes to it will be overwritten.*

Summary
-------

Rental Contract Insurance

Description
-----------

This module provides the opportunity to sell and invoice insurances related to the selled and invoiced rentable products.
The insurance price is either based on the product's costs or the order's amount and given as percentage.


Usage
-----

- Install the module.
- Open a rentable product and go to page Sale.
- Choose the calculation method for the insurance when renting this product and set the percentage.
- Create a sale order.
- Add a line with a product and see the default settings for the insurance.
- Save the sale order and see the newly added line for the insurance with the calculated price.


Changelog
---------

- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- a35a62d4 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- a0fba4ea 2020-12-03 19:46:27 +0100 yweng@elegosoft.com  (origin/feature_3477_blp862_rental_insurance_v12) [FIX] Unittest of module rental_contract_insurance
- 5ee8f035 2020-12-02 13:57:44 +0100 yweng@elegosoft.com  [IMP] add domain for insurance product in form view of sale order line
- a158a987 2020-11-07 19:21:06 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3477_blp849_rental_product_insurance_v12: addons-rental-vertical remotes/origin/feature_3477_blp849_rental_product_insurance_v12 - 62c3c1fdf9aed24e6bca69af849f84fc9868f6d1 [IMP] implements new tests for module rental_contract_insurance and delete old test of rental_product_insurance
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 62c3c1fd 2020-11-04 15:30:21 +0100 yweng@elegosoft.com  (origin/feature_3477_blp849_rental_product_insurance_v12, feature_3477_blp849_rental_product_insurance_v12) [IMP] implements new tests for module rental_contract_insurance and delete old test of rental_product_insurance
- d0c42669 2020-11-04 15:28:26 +0100 yweng@elegosoft.com  [IMP] adjust function to calculate the price of the insurance product and update the module description
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5c 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d8 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 01f2cdd1 2020-10-13 14:37:04 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3477_blp824_insurance_v12) issue #3477 replace product_id with insurance_product_id due to previous renaming of the field
- 836a14b4 2020-10-06 15:33:55 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3477_blp819_rental_product_insurance_v12) issue #3884 rename product_id to insurance_product_id for insurances on sale order lines
- 5a5d213b 2020-09-29 10:03:51 +0200 yweng@elegosoft.com  [FIX] delete uom_id and uom_po_id for demo insurance product
- 98d44b63 2020-09-28 02:15:47 +0200 yweng@elegosoft.com  [IMP] improve module for insurance
- 114c04ca 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- 6944ff44 2020-08-13 12:10:54 +0200 yweng@elegosoft.com  (origin/feature_3477_blp732_rental_product_insurance_v12) [IMP] improves insurance module for creating/updating more insurance lines (sale.order.line)
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 85703c8f 2020-06-11 14:46:38 +0200 yweng@elegosoft.com  [IMP] delete field insurance_amount of sale.order.line and change function _compute_insurance_amount to onchange_insurance_amount
- 8d86931a 2020-05-25 17:47:16 +0200 yweng@elegosoft.com  (origin/feature_3477_blp623_rental_product_insurance_v12) [IMP] add some translations for module rental_product_insurance and rental_contract_insurance
- 157939bb 2020-05-25 16:58:30 +0200 yweng@elegosoft.com  [IMP] improves unittests of module rental_contract_insurance and rental_product_insurance
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- cb28bea4 2020-05-19 18:05:47 +0200 yweng@elegosoft.com  (origin/feature_3477_blp602_rental_product_insurance_v12, feature_3477_blp602_rental_product_insurance_v12) [IMP] Extension of Rental Insurance 1. New Button on tree view to update/create insurance line 2. set product_uom_qty of Insurance by using number_of_time_unit or product_uom_qty / rental_qty of origin line 3. add function fields to calculate insurance_price_unit and insurance_amount
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 38953ec0 2020-04-30 17:42:35 +0200 yweng@elegosoft.com  (origin/feature_3477_blp521_rental_product_insurance_v12, feature_3477_blp521_rental_product_insurance_v12) [IMP] add some translations for module rental_contract_insurance
- 411a2835 2020-04-30 14:00:21 +0200 yweng@elegosoft.com  [IMP] adjust unit tests for module rental_product_insurance and rental_contract_insurance
- 2d48d5f5 2020-04-29 17:50:04 +0200 wagner@elegosoft.com  adapt contract count in test (issue #3615)
- df682021 2020-04-29 15:54:53 +0200 yweng@elegosoft.com  [FIX] function _prepare_invoice_line of sale.order.line
- 1ae485a4 2020-04-29 12:18:40 +0200 yweng@elegosoft.com  [IMP] adjusts insurance product and insurance contract product
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932a 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340dc 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b3 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d2 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- 44b59af8 2020-03-29 11:04:11 +0200 yweng@elegosoft.com  (origin/feature_3576_blp420_unittest_rental_contract_month_v12) [FIX] _create_rental_insurance_line
- 68f10332 2020-03-27 22:55:05 +0100 yweng@elegosoft.com  [FIX] key error by creating of sale.order.line
- bbea9f16 2020-03-24 20:27:11 +0100 yweng@elegosoft.com  (origin/feature_3593_blp412_rental_product_instance_v12) [ADD] module rental_contract_insurance

