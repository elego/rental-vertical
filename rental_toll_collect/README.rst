Rental Toll Collect
====================================================

*This file has been generated on 2022-07-26-13-09-49. Changes to it will be overwritten.*

Summary
-------

Import a CSV file from Toll Collect and invoice the costs to customers.

Description
-----------

This module provides the opportunity to import csv files downloaded from toll collect portal.
During import it matches the given license plate in csv file with a vehicle product.
The toll charge lines can be invoiced to a customer manually or by creating an invoice from a 
sale/rental order containing a vehicle product as sale/rental order line.

The csv should contain the following columns:

- Account number ("Mautaufstellungs-Nr.")
- license plate ("Kfz-Kennz.")
- Date ("Datum")
- Start	("Start")
- Booking number ("Buchungsnummer")
- Type ("Art")
- Route Ramp ("Auffahrt")
- Route Via ("über")
- Route Exit ("Abfahrt")
- Analytic Account ("Kostenstelle")
- Tariff Model ("Tarifmodell")
- Axle class ("Achsklasse")
- Weight class ("Gewichtsklasse")
- Polution class ("Schadstoffklasse")
- Road operator ("Straßenbetreiber")
- Procedure ("Verf.¹")
- Distance ("km")
- Amount ("EUR")


Usage
-----

-  Go to Rentals > Configuration > Settings
- Activate the automatic invoicing of toll charges if toll charges should be automatically invoiced together with rental services.
- Create a rental order with vehicle products as rental order lines.
- Confirm the rental order.
- Go to Rentals > Product > Toll Charges > Import Toll Charges.
- Upload your csv file and import the file.
- Go to Rentals > Product > Toll Charges > Toll Charge Lines and see all imported toll charge lines.
- Go to a vehicle product and click on smartbutton for toll charges and see all related toll charge lines.
- Go back to the rental order and create an invoice.
- If the date of the toll charge lines match the service period of rental order lines, 
  a new invoice line is additionally added for each vehicle product with distance and amount.

- Mark one or several toll charge lines in tree view and create an invoice via action wizard to invoice them manually.


Changelog
---------

- 2d6ba4d8 2022-05-23 12:38:59 +0200 cpatel@elegosoft.com  [IMP] refactor the dependencies in rental modules, (issue#4955)
- 1e549e87 2022-05-04 12:56:56 +0200 wagner@elegosoft.com  (origin/feature_2832_blp7_new_logos_v12, feature_2832_blp7_new_logos_v12) update doc (issue #3613, issue #4016)
- 02eb49c8 2022-05-04 12:18:32 +0200 wagner@elegosoft.com  update doc (issue #4016)
- 4ff94cf3 2022-05-04 12:09:50 +0200 wagner@elegosoft.com  add new rental logo (issue #3613, issue #4016)
- 214cf6a2 2022-04-27 15:13:48 +0200 cpatel@elegosoft.com  (origin/feature_4995_blp1380_refactor_fleet_extensions_v12) [FIX] test errors due to field license_plate and correct remaining ref after refactoring, (issue#4995)
- 296b6193 2021-10-25 10:20:28 +0200 wagner@elegosoft.com  regenrate documentation (issue #4016)
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- 3627532b 2021-06-25 15:21:10 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_4098_blp1110_rental_toll_collect_v12: addons-rental-vertical remotes/origin/feature_4098_blp1110_rental_toll_collect_v12 - e7f929dfe79aa6a5e128bd05ee84a15be145a7b8 [IMP] minor changes, (issue#4098)
- e7f929df 2021-06-16 11:31:29 +0200 cpatel@elegosoft.com  (origin/feature_4098_blp1110_rental_toll_collect_v12) [IMP] minor changes, (issue#4098)
- a285f3fd 2021-06-16 11:22:30 +0200 cpatel@elegosoft.com  [IMP] toll collect csv file import, filter rows before import(issue#4098)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- 5d777a60 2021-03-26 14:10:02 +0100 cpatel@elegosoft.com  (origin/feature_3903_blp1043_rental_toll_collect_v12) [IMP] add attachment only if any invoced toll charge lines, (issue#3903)
- 623366e6 2021-03-25 16:33:53 +0100 cpatel@elegosoft.com  [IMP] changes to rental_toll_collect, 1. added report for toll charge lines 2. add attachment only toll charge lines are available on account.invoice when user click on Send and Print ,(issue#3903)
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- a35a62d4 2020-12-22 22:59:30 +0100 kay.haeusler@elego.de  regenerate all de.po and \*.pot files; issue #4016
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- e1bdbc84 2020-12-10 15:10:08 +0100 cpatel@elegosoft.com  (origin/fix_3950_blp918_rental_toll_collect_v12) [FIX] set administrative_charge field default value to False for Company,(issue#3950)
- 363aa9be 2020-12-08 17:47:46 +0100 cpatel@elegosoft.com  (origin/feature_3950_blp906_rental_toll_collect_v12) [IMP] manage Administrative Charge product for rental_toll_collect, (issue#3950)
- 4be58b63 2020-11-27 13:45:12 +0100 maria.sparenberg@elegosoft.com  (defect_3950_blp862_rental_toll_collect_v12) issue #3950 set the charge product for all partners
- 6d611e73 2020-11-25 14:56:17 +0100 maria.sparenberg@elegosoft.com  issue #3950 add post_init_hook to set the administrative charge product to existing customers
- f2f49803 2020-11-24 17:27:51 +0100 maria.sparenberg@elegosoft.com  issue #3950 add invoicing of administrative charge in toll charge invoices
- 65da51fa 2020-11-24 17:22:39 +0100 maria.sparenberg@elegosoft.com  issue #3950 only invoice administrative charge if the invoice contains toll charge invoicing
- 0fb164b6 2020-11-24 16:58:35 +0100 maria.sparenberg@elegosoft.com  issue #3950 allow invoicing of toll charges from toll charge lines
- 3fb4883f 2020-11-19 17:01:56 +0100 kay.haeusler@elego.de  fix the missing comma in the onchange definition; issue #3950
- c7e3b592 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2af 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e8 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8c 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb502 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5c 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe52 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 86e7c1a6 2020-10-28 12:35:56 +0100 maria.sparenberg@elegosoft.com  issue #3613 add manifest description and usage for several rental modules
- 5244748e 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d8 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 2ab176f8 2020-10-15 11:13:24 +0200 cpatel@elegosoft.com  (origin/feature_3478_blp831_toll_collect_unittest_v12) [IMP] correct data to csv file,csv import unitest,issue#3478
- 5468f7b4 2020-10-14 14:35:31 +0200 cpatel@elegosoft.com  [IMP] improve coverage in unittest,issue#3478
- 810939cf 2020-10-13 15:37:40 +0200 cpatel@elegosoft.com  (origin/feature_3478_blp824_toll_collect_v12) [IMP] add unittest for modules rental_toll_collect,rental_contract_toll_collect,issue#3478
- eb83afb8 2020-10-13 13:43:26 +0200 maria.sparenberg@elegosoft.com  issue #3478 fix German translation and make product data not updateable
- 1f208a7b 2020-10-08 16:57:10 +0200 cpatel@elegosoft.com  [IMP] webtour added for rental_toll_collect,rental_contract_toll_collect module,issue#3478
- a96c78ad 2020-10-06 12:29:54 +0200 cpatel@elegosoft.com  (origin/feature_3478_blp819_toll_collect_v12) [IMP] fix rounding problem,change uom to Unit(s) of Toll Charges product,issue#3478
- e5a88c6e 2020-10-01 14:57:22 +0200 maria.sparenberg@elegosoft.com  issue #3478 fix write method in sale order line to avoid endless recursion
- 854fde23 2020-09-18 14:58:02 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3478_blp790_toll_collect_v12) issue #3478 update toll product invoice line when changing toll charge line
- f9354fd6 2020-09-17 17:03:22 +0200 maria.sparenberg@elegosoft.com  issue #3478 simplify invoicing of toll charge lines
- 3077707a 2020-09-16 16:37:06 +0200 maria.sparenberg@elegosoft.com  issue #3478 save toll line ids on sale order line and invoice line
- 0ba71cb5 2020-09-15 13:37:57 +0200 maria.sparenberg@elegosoft.com  issue #3478 sort toll charge lines by toll_date and fix translation
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- cf19f22c 2020-05-27 16:37:15 +0200 maria.sparenberg@elegosoft.com  issue #3478 fix some strings and update German translation
- 886e9b0a 2020-05-26 11:38:44 +0200 maria.sparenberg@elegosoft.com  issue #3478 show exception when more products are found with given license plate
- 2ceec0cc 2020-05-26 10:33:03 +0200 maria.sparenberg@elegosoft.com  issue #3478 fix toll charge line smartbutton in sale order and invoice
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 115d1760 2020-05-15 09:13:21 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3478_blp559_rental_toll_collect_v12) issue #3478 add toll charge invoice lines when creating invoice from sale order
- 5b7911ef 2020-05-14 16:05:37 +0200 maria.sparenberg@elegosoft.com  issue #3478 refactor the entire module
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- de1bb66b 2020-04-30 20:04:06 +0200 ycervantes@elegosoft.com  (origin/feature_3478_blp521_rental_toll_collect_v12, feature_3478_blp521_rental_toll_collect_v12) (issue #3478) handle import errors for toll collect
- 004f61f1 2020-04-29 18:54:00 +0200 ycervantes@elegosoft.com  (issue #3478) fix toll collect import
- 70c4b7df 2020-04-28 20:52:29 +0200 ycervantes@elegosoft.com  (origin/feature_3478_blp503_rental_toll_collect_v12) (issue #3478) fix labels and translations for the toll.charge.line fields
- c5ec7585 2020-04-28 09:17:04 +0200 cpatel@elegosoft.com  (origin/wip_3478_blp503_rental_toll_collect_v12) [ADD] rental_toll_collect : add new module , issue#3478

