Rental Contract Month
====================================================

*This file has been generated on 2020-10-27-14-49-15. Changes to it will be overwritten.*

Summary
-------

Extension of module rental_contract and rental_pricelist

Description
-----------

During longtime rentals, it is often required to write invoices in regular intervals.
This is possible with the contract module, which is here extended to support rental
use cases in extension to purchase and sale use cases.

If a product is rentable in months, the related rental service is automatically 
considered as a contract and linked to the standard customer contract template.
If you add this monthly rental service in a sale order and confirm it, a contract 
is automatically created.


Usage
-----

Create a stockable product and mark it as rentable in months.
The automatically created rental service has the flag 'Is a contract' = True.
Create a sale order, add the rental service and confirm the order.
A contract is automatically created.


Changelog
---------

- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (HEAD -> fix_3339_blp840_extend_documentation_v12, origin/rental_v12_integration, rental_v12_integration) update doc generation script (issue #3339)
- 114c04c 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 556210b 2020-04-29 14:02:37 +0200 yweng@elegosoft.com  [IMP] set display_product_id by creating of sale.order.line
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- bf019a3 2020-03-26 13:16:32 +0100 yweng@elegosoft.com  [IMP] unittest for rental_contract_month
- 6fa2772 2020-03-24 20:26:41 +0100 yweng@elegosoft.com  [FIX] rental_contract_month
- ea35976 2020-03-18 13:06:04 +0100 maria.sparenberg@elegosoft.com  issue #3589 move fields to correct groups in module rental_contract
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 9576b54 2020-03-09 14:32:43 +0100 wagner@elegosoft.com  (origin/fix_3339_blp343_extend_documentation_v12, fix_3339_blp343_extend_documentation_v12) allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 54e4ad1 2020-03-09 11:57:52 +0100 maria.sparenberg@elegosoft.com  issue #3467 add usage section for rental_contract_month
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462
- 18aa004 2020-03-04 11:38:44 +0100 yweng@elegosoft.com  (origin/feature_3563_blp311_rental_contract_v12) [ADD] module rental_contract_month

