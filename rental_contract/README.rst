Rental Contract
====================================================

*This file has been generated on 2021-10-25-10-18-19. Changes to it will be overwritten.*

Summary
-------

Extension of module contract for rental use cases

Description
-----------

During longtime rentals, it is often required to write invoices in regular intervals.
This is possible with the contract module, which is here extended to support rental
use cases in extension to purchase and sale use cases.

The module adds subtypes for contracts in order to distinguish between customer contracts, 
customer rental contracts, vendor contracts and vendor rental contracts. 
It is possible to add more subtypes with own sequence, which automatically sets the contract's code.

- If a contract is automatically created from sale order, it passes the sale order type to the contract subtype.
- The analytic account of a product is automatically set on the contract line.
- The start and end date of invoice lines are automatically set when creating the invoice from a contract.
- Both fields date_start and date_end that are used for contract lines are now hidden and related to the given 
  start and end date of sale order line.


Usage
-----

You can add new contract subtypes here:

 - Invoicing > Configuration > Contract > Contract Subtypes
 - Rentals > Configuration > Contract > Contract Subtypes
 
 - Create a sale order.
 - Choose a sale type.
 - Add a rental product that has a rental service marked as contract with a contract template 
   and an analytic income account.
 - Choose a service period by setting start and end date.
 - Confirm the order.
 - Check the automatically created contract for contract type, analytic accounts, ...

This module is automatically installed when all of the following modules are installed in a database:

 - contract
 - product_contract
 - sale_start_end_dates
 - sale_rental
 - rental_base


Changelog
---------

- 43b06373 2021-10-10 18:18:11 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4447_blp1142_rental_product_variant_v12: addons-rental-vertical remotes/origin/feature_4447_blp1142_rental_product_variant_v12 - 35019a0969ffa6b2625ae89220590787266e85d7 [IMP] improve domain on smart buttons on Product.product form view, so inactivated product or related inactivated rental services also covered, (issue#4447)
- 35019a09 2021-09-29 09:47:59 +0200 cpatel@elegosoft.com  (origin/feature_4447_blp1142_rental_product_variant_v12) [IMP] improve domain on smart buttons on Product.product form view, so inactivated product or related inactivated rental services also covered, (issue#4447)
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- cef8bcb6 2021-06-25 15:21:15 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4273_blp1110_rental_product_pack_v12: addons-rental-vertical remotes/origin/feature_4273_blp1110_rental_product_pack_v12 - 8b3f8264d894702df1b16242fefa3f48425f7f43 [IMP] improve german translation,to rental_contract (issue#3920)
- 8b3f8264 2021-06-25 10:56:18 +0200 cpatel@elegosoft.com  (origin/feature_4273_blp1110_rental_product_pack_v12) [IMP] improve german translation,to rental_contract (issue#3920)
- 1bef043c 2021-06-23 12:02:44 +0200 cpatel@elegosoft.com  [IMP] add filters for end_date on contract list view,same like timesheet, (issue#3920)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 1abc79fe 2021-05-12 18:08:04 +0200 yweng@elegosoft.com  (origin/wip_4168_sale_rental_v12, wip_4168_sale_rental_v12) [IMP] adjust dependence of rental modules: replace rental_sale with sale_rental
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- a35a62d4 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5c 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 81de96e2 2020-10-28 12:42:53 +0100 wagner@elegosoft.com  resolve conflicts (issue #3613)
- 86e7c1a6 2020-10-28 12:35:56 +0100 maria.sparenberg@elegosoft.com  issue #3613 add manifest description and usage for several rental modules
- 5d1c1064 2020-10-28 11:51:40 +0100 wagner@elegosoft.com  add several usage notes for auto-installing modules (issue #3613)
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d8 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- adcc40f7 2020-10-07 10:19:08 +0200 maria.sparenberg@elegosoft.com  (origin/defect_3878_blp824_update_times_v12) issue #3878 fix arguments for update times because start date was also written as end date
- b4743f79 2020-10-05 16:13:02 +0200 maria.sparenberg@elegosoft.com  (origin/defect_3880_blp819_timeline_confirmed_so_v12) issue #3880 allow updating confirmed order lines and corresponding timeline entries and contract lines
- 354454eb 2020-10-05 11:44:44 +0200 maria.sparenberg@elegosoft.com  issue #3880 create contract line for sale order line that are created in order state 'sale'
- 1be4b54c 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 114c04ca 2020-09-11 15:36:33 +0200 yweng@elegosoft.com  (origin/feature_3822_blp790_duplicated_fields_v12) [MIG] Model 'product.template': replace rental_ok with rental
- 74abd2c7 2020-09-02 13:27:59 +0200 yweng@elegosoft.com  (origin/feature_3766_blp753_rental_partner_contract_smartbutton_v12) [IMP] adjust Menus for contracts
- 1f1c56bc 2020-08-07 18:20:49 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/defect_3782_blp721_contract_date_start_end_v12: addons-rental-vertical remotes/origin/defect_3782_blp721_contract_date_start_end_v12 - df1d31f48e3af1b19c358847178bb19dca77dcbb [FIX] adjust date_start and date_end of sale.order.line for contract
- 48b7e28a 2020-08-05 12:05:53 +0200 yweng@elegosoft.com  (origin/feature_3816_blp721_quotation_order_menu_v12) [IMP] do not use sale_order_type.normal_sale_type to search the sale.order
- df1d31f4 2020-08-04 20:30:01 +0200 yweng@elegosoft.com  (origin/defect_3782_blp721_contract_date_start_end_v12) [FIX] adjust date_start and date_end of sale.order.line for contract
- 4153ab5c 2020-07-14 22:11:26 +0200 yweng@elegosoft.com  (origin/defect_3765_blp700_product_smartbuttons_v12) [IMP] Adjust smartbutton of product
- d0f0a58e 2020-07-10 13:44:37 +0200 cpatel@elegosoft.com  (origin/fix_3765_blp689_rental_product_smartbuttons_count_v12) [FIX] smartbuttons count,Rental,C-Contract,issue#3765
- 8f8aff90 2020-07-07 18:22:30 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/defect_3748_blp677_related_date_start_date_end_v12: addons-rental-vertical remotes/origin/defect_3748_blp677_related_date_start_date_end_v12 - 8861135e68a74179e3ac3feff23a016fc9950df9 [IMP] fixes tour test rental_contract_tour
- 42fc9eb3 2020-07-02 15:08:31 +0200 yweng@elegosoft.com  [IMP] overwrite field date_start and date_end als related fields
- 3737cf93 2020-07-01 14:42:54 +0200 maria.sparenberg@elegosoft.com  (origin/fix_3747_blp677_fix_contract_creation_v12) issue #3747 remove readonly attribute for contract types
- 511d200f 2020-07-01 13:58:08 +0200 maria.sparenberg@elegosoft.com  (origin/fix_3747_blp760_fix_contract_creation_v12) issue #3747 fix exception when confirming a sale order with new sale / contract type
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- becbdc22 2020-04-30 18:19:12 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3477_blp521_rental_product_insurance_v12: addons-rental-vertical remotes/origin/feature_3477_blp521_rental_product_insurance_v12 - 38953ec05f7f92504519d0eb7b3060457e8ebac3 [IMP] add some translations for module rental_contract_insurance
- df682021 2020-04-29 15:54:53 +0200 yweng@elegosoft.com  [FIX] function _prepare_invoice_line of sale.order.line
- e1ac7d7b 2020-04-29 09:42:21 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3467_blp521_hide_auto_renew_v12) issue #3467 hide boolean field for contract auto renew in rentals
- d155b443 2020-04-27 09:21:28 +0200 cpatel@elegosoft.com  (origin/fix_3615_blp503_invoice_service_period_v12) [FIX] reantal_contract : remove date_start and date_end(service period od Invoice) ref comes from ROCKBIRD repo,issue#3615
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- fa906684 2020-04-22 11:54:09 +0200 cpatel@elegosoft.com  (origin/fix_3615_blp488_branch_name_v12) [FIX] remove ref of branch_name
- 38ff173e 2020-04-22 11:33:31 +0200 yweng@elegosoft.com  [IMP] delete branch_name in function _prepare_invoice
- 7fac932a 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340dc 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b3 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d2 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- ff31876b 2020-03-30 17:55:07 +0200 cpatel@elegosoft.com  [IMP] renatl_contract,rental_pricelist todo points(ticket#3467,ticket#3589) 1. ticket#3467, set the code of automatically created contracts from sale order to the sale order number if the contract subtype has no sequence 2. ticket#3589, The computation of number_of_time_unit is not correct when using the uom Month(s)
- c670a5f2 2020-03-21 13:07:52 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3589_blp400_rental_order_v12) issue #3589 remove start and end date from sale order line tree view
- ea359764 2020-03-18 13:06:04 +0100 maria.sparenberg@elegosoft.com  issue #3589 move fields to correct groups in module rental_contract
- 823d4c78 2020-03-17 20:06:15 +0100 maria.sparenberg@elegosoft.com  issue #3589 improve sale order (line) view in rental_base module
- b49c01da 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e942 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 977d2245 2020-03-13 10:58:32 +0100 cpatel@elegosoft.com  (origin/feature_3279_blp371_todo_points_v12) [IMP] todo points issue # 3279
- e371276d 2020-03-10 18:14:07 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- f04eb22d 2020-03-10 10:53:09 +0100 cpatel@elegosoft.com  (origin/feature_3563_blp343_rental_contract_v12) [IMP] set analytic account,branch name,service period when create invoice from sale order
- e6f3fb42 2020-03-09 14:46:29 +0100 cpatel@elegosoft.com  [IMP] todo points issue #3563    1. add a domain on 'contract_type_id’ in invoices in order to show only customer or vendor contracts
- 9576b54f 2020-03-09 14:32:43 +0100 wagner@elegosoft.com  (origin/fix_3339_blp343_extend_documentation_v12, fix_3339_blp343_extend_documentation_v12) allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 7ea29f46 2020-03-09 14:07:06 +0100 cpatel@elegosoft.com  [IMP] todo points issue #3467    1. pass the values 'default_start_date’ from sale order to 'date_start’ in invoice    2. pass the values 'default_end_date’ from sale order to 'date_end’ in invoice    3. change the view for default_start_date and default_end_date by adding       a label 'Service Period’ as per Invoice(include German Transaltion)    4. pass the value for branch name from sale order to invoice
- c97bd4bd 2020-03-09 11:01:59 +0100 maria.sparenberg@elegosoft.com  issue #3462 add usage section for rental_contract
- d0891199 2020-03-09 11:47:19 +0100 maria.sparenberg@elegosoft.com  issue #3563 add menu item in rentals menu for contract subtypes
- d66cf184 2020-03-09 11:01:59 +0100 maria.sparenberg@elegosoft.com  issue #3462 add usage section for rental_contract
- 804dc443 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6f170ba7 2020-03-05 13:38:38 +0100 cpatel@elegosoft.com  (origin/feature_3563_blp326_rental_contract_v12) [IMP] remove default value of contract_type on customer invoice form
- 994ee02f 2020-03-05 13:18:30 +0100 cpatel@elegosoft.com  [IMP] todo points for rental_contract module
- 4c76ef2b 2020-03-04 16:56:16 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp311_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp311_extend_documentation_v12 - 7dde7fa1ec109919795e59198feb24fc96fcfeb1 add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 45e01042 2020-03-04 11:38:21 +0100 yweng@elegosoft.com  [IMP] simplify configuration of contract product
- eaaabc57 2020-03-04 11:08:07 +0100 cpatel@elegosoft.com  [IMP] revert changes: set code of contract with name of the rental order
- 7d151993 2020-03-03 16:36:01 +0100 yweng@elegosoft.com  [IMP] set code of contract with name of the rental order
- 334d3e81 2020-03-03 16:24:08 +0100 yweng@elegosoft.com  [IMP] set analytic_account_id of contract_line in function _prepare_contract_line_values()
- 58079cca 2020-03-03 16:22:35 +0100 yweng@elegosoft.com  [FIX] function _prepair_invoice_line of contract.line
- bb889476 2020-03-03 16:50:16 +0100 cpatel@elegosoft.com  [IMP] view correction
- bb1f523c 2020-03-03 16:19:24 +0100 cpatel@elegosoft.com  [IMP] contract.order.type for sale order(noraml,rental)
- 6bcb6e6f 2020-03-03 16:57:04 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp311_refactoring_menus_v12) Menu refactoring; issue #3462
- 7dde7fa1 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c9 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- 1db47608 2020-02-29 23:48:15 +0100 wagner@elegosoft.com  add some more simple module decsriptions (issue #3339)
- 6965ed1c 2020-02-29 22:46:34 +0100 wagner@elegosoft.com  fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- 4d17de41 2020-02-11 16:30:49 +0100 yweng@elegosoft.com  [IMP] adjusts smartbuttons of product variant
- a88dfb52 2020-02-12 12:57:10 +0100 yweng@elegosoft.com  [IMP] refactoring of menus
- b266b328 2020-02-11 12:48:49 +0100 maria.sparenberg@elegosoft.com  (origin/feature_3467_blp236_contract_German_translation_v12) issue #3467 add German translations
- 7c2d9c5c 2020-02-10 16:31:07 +0100 yweng@elegosoft.com  (origin/feature_3467_blp214_rental_contract_v12) [IMP] add smart button for supplier contracts and customer contracts in product form view
- d11b4d99 2020-02-06 15:07:06 +0100 yweng@elegosoft.com  [IMP] adjust view for fields date_end and date_start of sale.order.line
- 94e76bbb 2020-01-23 13:08:03 +0100 yweng@elegosoft.com  [IMP] set liscense, copyrights and author
- 5188db94 2020-01-22 20:51:43 +0100 yweng@elegosoft.com  [ADD] add module rental_contract

