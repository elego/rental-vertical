Rental Product Instance
====================================================

*This file has been generated on 2023-02-19-14-17-56. Changes to it will be overwritten.*

Summary
-------

Add product instances identified by serial number as unique rented objects

Description
-----------

This module extends the product data model in order to mark them as unique product instances 
that are traced by serial number. You might have several instances of a product but they are 
in different conditions or are somehow unique like machines, vehicles or maybe 'used' products.

In order to track the condition history of a product instance you can add operating data, e.g.
you can save the mileage of vehicles or the operating hours of machines.


Usage
-----

- Install the module.
- Create a stockable product.
- Mark the product as product instance.
- Save the product and set an unique serial number.
  Hint: Make an inventory adjustment, if needed.
- Set a product category that can be configured to either use mileage or operating hours as condition.
- Go to the smartbutton for operating data, create the current condition and update it regularly.


Changelog
---------

- c92a1b33 2022-05-04 12:54:10 +0200 wagner@elegosoft.com  update doc (issue #3613, issue #4016)
- 19e327a4 2022-04-18 14:45:33 +0000 jenkins-ci@elegosoft.com  add new rental logo and update doc (issue #3613, issue #4016)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 279539a5 2022-03-14 10:48:31 +0100 cpatel@elegosoft.com  [IMP] correction,migration,fix unit test errors, (issue#4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

