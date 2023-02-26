Rental Check Availability
====================================================

*This file has been generated on 2023-02-19-14-17-56. Changes to it will be overwritten.*

Summary
-------

Extends the sale_rental module for checking availability of the rented product.

Description
-----------

This module activates availability checks on stockable products related to rental services in
sale orders. In the base functionality only the total amount of products in stock is checked and user is
informed when the amount of products to rent out in a sale order is higher.

After the installation of this module the availability is checked in consideration of the total amount
of goods in stock and the amount of products used in concurrent sale orders at the certain desired timeframe.
In case of insufficient products in stock the user receives visual notification on respective sale order line
and can access the list of concurrent sale orders directly.


Usage
-----

To use this module, you need to:

#. Go to Rental Orders and create a new one.

#. Add a product available for being rented out in sale order line.

#. If there is not enough stock on hand to fullfil the order and
   possible concurrent ones the sale order line will be colorized.
   Yellow marks that there are concurrent quotations and red indicates
   concurrent orders.

#. To check the concurrent order for a critical sale order line just click
   on the inline button being displayed in the sale order line.

Changelog
---------

- c92a1b33 2022-05-04 12:54:10 +0200 wagner@elegosoft.com  update doc (issue #3613, issue #4016)
- 19e327a4 2022-04-18 14:45:33 +0000 jenkins-ci@elegosoft.com  add new rental logo and update doc (issue #3613, issue #4016)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

