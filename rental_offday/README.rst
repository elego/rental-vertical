Rental Off Day
====================================================

*This file has been generated on 2020-10-28-16-15-18. Changes to it will be overwritten.*

Summary
-------

Calculate off-days in rentals on daily basis

Description
-----------

During short-term rentals over several days or weeks, the customer and the salesman 
agree on so called off-days. On these days the customer still have the rented products 
but usually doesn't use them and, therefore, does not pay the daily price. This is often 
the case for weekends and holidays, since there might be some legal limitations in using 
the products on these days.
In order to meet this requirement, the salesman can add off-days on sale order lines for 
products that are rentable in days. These days will not be included in price calculation.


Usage
-----

The off-days can only be used for products rentable in days.

- Create a stockable product and activate that it is rentable in days.
- Adjust its stock in location 'Rental In'.
- Create a sale order and rent out the product in days.
- Set a start and end date, e.g. for 3 weeks.
- On sale order line you will see a page 'Off-Days'.
- Choose the type 'Weekend' in order to create 'Fixed Off-Days' and you get a list with all saturdays 
  and sundays within the rental period.   
- Add some additional off-days.
- The number of off-days reduces the rental quantity and is therefore not included in price calculation.


Changelog
---------

- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  (HEAD -> v12, origin/v12) regenerate doc (issue #3613)
- 86e7c1a 2020-10-28 12:35:56 +0100 maria.sparenberg@elegosoft.com  issue #3613 add manifest description and usage for several rental modules
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 114c04c 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- 7a4cfcb 2020-09-11 11:28:47 +0200 maria.sparenberg@elegosoft.com  issue #3602 fix duplicated labels in module rental_offday
- eee2472 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 92cd0c0 2020-06-02 14:22:31 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3674_blp631_rental_offday_v12) issue #3674 add description to datamodel rental.offday
- 57b29fa 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340d 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- a26a41c 2020-03-18 13:58:55 +0100 maria.sparenberg@elegosoft.com  issue #3589 move fields to correct groups in module rental_offday
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- e371276 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- b454e5d 2020-03-10 18:14:06 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3576_blp343_unittest_rental_offday_v12: addons-rental-vertical remotes/origin/feature_3576_blp343_unittest_rental_offday_v12 - d9313d98f1961b9291fd769e4cbb1d56a567f97b issue #3576 add unittest for rental_offday
- d9313d9 2020-03-10 14:53:00 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3576_blp343_unittest_rental_offday_v12) issue #3576 add unittest for rental_offday
- 9576b54 2020-03-09 14:32:43 +0100 wagner@elegosoft.com  (origin/fix_3339_blp343_extend_documentation_v12, fix_3339_blp343_extend_documentation_v12) allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 81eb48d 2020-03-09 12:51:45 +0100 maria.sparenberg@elegosoft.com  issue #3287 add description and usage section for rental_offday
- f01d189 2020-03-09 12:51:45 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3287_blp343_rental_offday_v12) issue #3287 add description and usage section for rental_offday
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462

