Rental Contract Insurance
====================================================

*This file has been generated on 2020-10-28-16-58-04. Changes to it will be overwritten.*

Summary
-------

Rental Contract Insurance

Description
-----------

TODO


Changelog
---------

- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  (HEAD -> v12, origin/v12) add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 01f2cdd 2020-10-13 14:37:04 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3477_blp824_insurance_v12) issue #3477 replace product_id with insurance_product_id due to previous renaming of the field
- 836a14b 2020-10-06 15:33:55 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3477_blp819_rental_product_insurance_v12) issue #3884 rename product_id to insurance_product_id for insurances on sale order lines
- 5a5d213 2020-09-29 10:03:51 +0200 yweng@elegosoft.com  [FIX] delete uom_id and uom_po_id for demo insurance product
- 98d44b6 2020-09-28 02:15:47 +0200 yweng@elegosoft.com  [IMP] improve module for insurance
- 114c04c 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- 6944ff4 2020-08-13 12:10:54 +0200 yweng@elegosoft.com  (origin/feature_3477_blp732_rental_product_insurance_v12) [IMP] improves insurance module for creating/updating more insurance lines (sale.order.line)
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 85703c8 2020-06-11 14:46:38 +0200 yweng@elegosoft.com  [IMP] delete field insurance_amount of sale.order.line and change function _compute_insurance_amount to onchange_insurance_amount
- 8d86931 2020-05-25 17:47:16 +0200 yweng@elegosoft.com  (origin/feature_3477_blp623_rental_product_insurance_v12) [IMP] add some translations for module rental_product_insurance and rental_contract_insurance
- 157939b 2020-05-25 16:58:30 +0200 yweng@elegosoft.com  [IMP] improves unittests of module rental_contract_insurance and rental_product_insurance
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- cb28bea 2020-05-19 18:05:47 +0200 yweng@elegosoft.com  (origin/feature_3477_blp602_rental_product_insurance_v12, feature_3477_blp602_rental_product_insurance_v12) [IMP] Extension of Rental Insurance 1. New Button on tree view to update/create insurance line 2. set product_uom_qty of Insurance by using number_of_time_unit or product_uom_qty / rental_qty of origin line 3. add function fields to calculate insurance_price_unit and insurance_amount
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 38953ec 2020-04-30 17:42:35 +0200 yweng@elegosoft.com  (origin/feature_3477_blp521_rental_product_insurance_v12, feature_3477_blp521_rental_product_insurance_v12) [IMP] add some translations for module rental_contract_insurance
- 411a283 2020-04-30 14:00:21 +0200 yweng@elegosoft.com  [IMP] adjust unit tests for module rental_product_insurance and rental_contract_insurance
- 2d48d5f 2020-04-29 17:50:04 +0200 wagner@elegosoft.com  adapt contract count in test (issue #3615)
- df68202 2020-04-29 15:54:53 +0200 yweng@elegosoft.com  [FIX] function _prepare_invoice_line of sale.order.line
- 1ae485a 2020-04-29 12:18:40 +0200 yweng@elegosoft.com  [IMP] adjusts insurance product and insurance contract product
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- 44b59af 2020-03-29 11:04:11 +0200 yweng@elegosoft.com  (origin/feature_3576_blp420_unittest_rental_contract_month_v12) [FIX] _create_rental_insurance_line
- 68f1033 2020-03-27 22:55:05 +0100 yweng@elegosoft.com  [FIX] key error by creating of sale.order.line
- bbea9f1 2020-03-24 20:27:11 +0100 yweng@elegosoft.com  (origin/feature_3593_blp412_rental_product_instance_v12) [ADD] module rental_contract_insurance
