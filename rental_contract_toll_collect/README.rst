Rental Contract Toll Collect
====================================================

*This file has been generated on 2021-10-25-10-18-19. Changes to it will be overwritten.*

Summary
-------

Invoice toll charge lines to customers periodically by contract usage.

Description
-----------

This module is an extension of rental_toll_collect. When using contracts for periodic 
invoicing of rental orders, this module provides the opportunity to also invoice the 
toll charges for the given time period.


Usage
-----

- Create a rental order with vehicle products as rental order lines.
- The products needs to be rented out in months in order to automatically create the contract.
- Confirm the rental order and see the newly created contract.
- Import the csv-file downloaded from Toll Collect Portal in order to create toll charge lines.
- The cronjob will automatically create invoices for this contract.
- If the date of the imported toll charge lines match the service period of invoice lines to be created, 
  a new invoice line with the toll product is additionally added for each vehicle product with distance and amount.

This module is automatically installed when all of the following modules are installed in a database:

- rental_toll_collect
- rental_contract_month


Changelog
---------

- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- a35a62d4 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- f2f49803 2020-11-24 17:27:51 +0100 maria.sparenberg@elegosoft.com  issue #3950 add invoicing of administrative charge in toll charge invoices
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
- 08ed05cf 2020-10-15 14:31:48 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3627_blp831_correction_unittest_v12: addons-rental-vertical remotes/origin/feature_3627_blp831_correction_unittest_v12 - a32f3cf469a9259957ef47bcd0fa8b64a0c8be2d [IMP] correct unitest errors, module:rockbird_product_description,issue#3627
- a32f3cf4 2020-10-14 18:06:26 +0200 cpatel@elegosoft.com  (origin/feature_3627_blp831_correction_unittest_v12) [IMP] correct unitest errors, module:rockbird_product_description,issue#3627
- 5468f7b4 2020-10-14 14:35:31 +0200 cpatel@elegosoft.com  [IMP] improve coverage in unittest,issue#3478
- 810939cf 2020-10-13 15:37:40 +0200 cpatel@elegosoft.com  (origin/feature_3478_blp824_toll_collect_v12) [IMP] add unittest for modules rental_toll_collect,rental_contract_toll_collect,issue#3478
- ee82daa5 2020-10-01 18:50:17 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3478_blp804_toll_collect_v12) issue #3478 update toll line ids before creating an invoice from contract
- 854fde23 2020-09-18 14:58:02 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3478_blp790_toll_collect_v12) issue #3478 update toll product invoice line when changing toll charge line
- f9354fd6 2020-09-17 17:03:22 +0200 maria.sparenberg@elegosoft.com  issue #3478 simplify invoicing of toll charge lines
- d4f54d81 2020-09-16 16:39:44 +0200 maria.sparenberg@elegosoft.com  issue #3478 simplify search for toll collect lines in contracts
- 0ba71cb5 2020-09-15 13:37:57 +0200 maria.sparenberg@elegosoft.com  issue #3478 sort toll charge lines by toll_date and fix translation
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- f5146b16 2020-05-27 16:50:29 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3478_blp623_rental_toll_collect_v12) issue #3478 module to invoice toll charge lines from contracts

