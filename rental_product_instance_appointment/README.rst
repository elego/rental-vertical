Rental Product Instance Appointment
====================================================

*This file has been generated on 2022-05-04-12-55-06. Changes to it will be overwritten.*

Summary
-------

Rental Product Instance Appointment

Description
-----------

Product instances are unique products in a current state and some tasks needs to be regularly done with them.
This module provides the possibility to add single or recurrent appointments for a product which automatically
create project tasks a defined time before the actual appointment date.

You can distinguish between time dependent and usage dependent appointments.
Time dependent appointments are due on a specific date.
Usage dependent appointments are due if a specific condition is reached,
like a certain mileage or amount of operating hours.


Usage
-----

- Create a product instance.

- Add one or several time dependent appointments in 'Appointments' page on product view.
- Set a name, date, a notification lead time (in days) and a time interval for each appointment.
- Before the appointment is due a project task will be created automatically by a cronjob using the lead time.
- If the appointment date is today, the next appointment is calculated by the intervall.

- Add one or several usage dependent appointments in 'Appointments' page on product view.
  The product instance therefore need a condition type configured by its product category.
- Set a name, a threshold, an intervall, a notification lead time (in days) and a daily increase.
- If there are no existing operating data yet, the daily increase is by default 1 and the appointment
  date is calculated using 'today' as a reference until the threshold is reached.
- If there are operating data, the daily increase is calculated from the value and date difference,
  using the last 20 operating data that differ in value and time.
- A project task is automatically created before the calculated appointment date using the lead time.


Changelog
---------

- 02eb49c8 2022-05-04 12:18:32 +0200 wagner@elegosoft.com  update doc (issue #4016)
- 4ff94cf3 2022-05-04 12:09:50 +0200 wagner@elegosoft.com  add new rental logo (issue #3613, issue #4016)
- fe0abaf8 2022-01-14 13:07:48 +0100 maria.sparenberg@elegosoft.com  issue #4552 fix dependency
- 296b6193 2021-10-25 10:20:28 +0200 wagner@elegosoft.com  regenrate documentation (issue #4016)
- 8b4d40c4 2021-09-23 09:19:24 +0200 wagner@elegosoft.com  regenerate doc (issue #4016)
- a5ae96f3 2021-06-25 15:21:08 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/feature_3924_blp1110_product_instance_appointment_v12: addons-rental-vertical remotes/origin/feature_3924_blp1110_product_instance_appointment_v12 - 05df4ef2660dcd9427b6fd8d8c7f9f3c499dbb8e [IMP] Add related fields of last apointment to show its state and color in tree view of appointments (issue 3924)
- 05df4ef2 2021-06-24 12:06:02 +0200 yweng@elegosoft.com  (origin/feature_3924_blp1110_product_instance_appointment_v12, origin/feature_3924_blp1102_product_instance_appointment_v12) [IMP] Add related fields of last apointment to show its state and color in tree view of appointments (issue 3924)
- dd988a2f 2021-06-09 12:42:47 +0200 wagner@elegosoft.com  update documentation (issue #3613)
- bbd5cb25 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- 83ed8f72 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
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
- 6cabea01 2020-10-16 13:01:37 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3641_blp833_usage_dependent_appointments_v12) issue #3641 skip operating data for calculation if their value has not changed
- 48b24a29 2020-10-16 12:52:26 +0200 maria.sparenberg@elegosoft.com  issue #3641 fix calculation for next appointment by using the most current date of operating data (not today)
- 215794a0 2020-10-16 10:56:58 +0200 maria.sparenberg@elegosoft.com  issue #3641 fix calculation for daily increase in case of several newly created operating data daily
- 1674a059 2020-10-15 14:02:04 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3641_blp831_appointment_v12) issue #3641 change field types for operating data
- 10b5ea79 2020-10-13 17:12:33 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3641_blp824_rental_product_instance_appointment_v12) issue #3641 fix calculation of next service appointment
- 3aa58fa7 2020-10-13 16:30:45 +0200 cpatel@elegosoft.com  [IMP] fix error: product.appointment has no attribute date_last_appointment while rental click tour,issue#3641
- 3ebccf62 2020-10-07 14:52:41 +0200 yweng@elegosoft.com  [IMP] product_instance_appointment (issue 3641)
- 28d8db3f 2020-09-24 13:44:11 +0200 yweng@elegosoft.com  (origin/feature_3641_blp790_rental_product_instance_appointment_v12) [IMP] set default value for field daily_increase of product.operating.appointment
- 3505813a 2020-09-10 12:04:31 +0200 yweng@elegosoft.com  (origin/feature_3641_blp778_rental_product_instance_appointment_v12) [IMP] add cron job to update the operating appointments and create project tasks
- 413b6387 2020-09-10 11:16:08 +0200 maria.sparenberg@elegosoft.com  issue #3641 update German translations for rental_product_instance_appointment
- eb475765 2020-09-10 09:33:41 +0200 yweng@elegosoft.com  [IMP] Product Instance Appointment
- eee2472b 2020-06-26 19:24:51 +0200 wagner@elegosoft.com  (origin/fix_3339_blp669_extend_documentation_v12, origin/fix_3339_blp666_extend_documentation_v12, fix_3339_blp669_extend_documentation_v12, fix_3339_blp666_extend_documentation_v12) update documentation (issue #3339)
- 57b29fa1 2020-05-24 12:58:49 +0200 wagner@elegosoft.com  (origin/fix_3339_blp622_extend_documentation_v12, origin/fix_3339_bl616_extend_documentation_v12, fix_3339_blp622_extend_documentation_v12, fix_3339_bl616_extend_documentation_v12) update documentation for fix release (issue #3339)
- 94dc79ca 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf3 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- bb264cf0 2020-05-04 14:11:21 +0200 maria.sparenberg@elegosoft.com  (origin/feature_3421_blp542_appointments_v12) issue #3421 fix some typos and update German translation
- 134218b1 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 43e76d8b 2020-04-27 13:44:56 +0200 yweng@elegosoft.com  (origin/feature_3421_blp503_rental_product_instance_appointment_v12) [IMP] add new field 'last_task_id' for product.appointment
- 795b1b6a 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932a 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 2da340dc 2020-04-13 14:11:24 +0200 wagner@elegosoft.com  change license for rental-vertical to AGPL (issue #3339)
- 6d3410b3 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d2 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- 3119cfd8 2020-03-18 10:07:48 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp384_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp384_extend_documentation_v12 - b49c01dabbc653a42b77f82bd3c44a8759721359 regenerate doc (issue #3339)
- c71ec77e 2020-03-18 10:31:23 +0100 yweng@elegosoft.com  (origin/feature_3576_blp384_unittest_instance_appointment_v12) [IMP] delete debug functions in unittests
- 887b30d2 2020-03-16 23:11:31 +0100 yweng@elegosoft.com  [IMP] formatting module rental_product_instance_appointment
- 9e28e0b5 2020-03-16 22:33:06 +0100 yweng@elegosoft.com  [IMP] unittests of module product_instance_appointment
- a8e33851 2020-03-16 22:30:45 +0100 yweng@elegosoft.com  [IMP] move product_uom_month from rental_pricelist into rental_base
- b49c01da 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e942 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 9576b54f 2020-03-09 14:32:43 +0100 wagner@elegosoft.com  (origin/fix_3339_blp343_extend_documentation_v12, fix_3339_blp343_extend_documentation_v12) allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 07b0ce01 2020-03-09 14:18:04 +0100 maria.sparenberg@elegosoft.com  issue #3421 add description and usage section for rental_product_instance_appointment
- 804dc443 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 6fd1771a 2020-03-06 20:32:25 +0100 kay.haeusler@elego.de  (origin/feature_3462_blp333_renaming_addons_v12) rename and split some addons; issue #3462
- fc3b3089 2020-03-05 16:12:50 +0100 maria.sparenberg@elegosoft.com  issue #3287 fix description and help texts, add German translation
- 4c76ef2b 2020-03-04 16:56:16 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_3339_blp311_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp311_extend_documentation_v12 - 7dde7fa1ec109919795e59198feb24fc96fcfeb1 add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 5689f699 2020-03-03 18:25:54 +0100 yweng@elegosoft.com  [FIX] singleton error
- 7dde7fa1 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 4dc1d530 2020-02-28 18:13:49 +0100 yweng@elegosoft.com  (origin/feature_3421_blp297_rental_product_instance_appointment_v12) [ADD] module rental_product_instance_appointment

