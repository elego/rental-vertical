Rental Product Set
====================================================

*This file has been generated on 2022-05-04-12-21-41. Changes to it will be overwritten.*

Summary
-------

Extends the sale_product_set to add rented product set on sale order lines.

Description
-----------

Product sets define a number of products that are frequently sold together and are added
as different sale order lines. This modules extends this use case to renting of product
sets. As in the original workflows, independent rental order lines are created for all
the products in the set. There is no further relation between those products.


Usage
-----

Refer to the usage information of the OCA module sale_product_set to learn how to
define product sets.

This module extends the sale and stock functionality to enable the renting of
OCA product sets. In order to do that, just install the module.

No further configuration is needed.


Changelog
---------

- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- 0cfd4773 2022-03-01 17:01:16 +0100 cpatel@elegosoft.com  [IMP] parameter correction, (issue#4516)
- b5dd7aac 2022-03-01 13:56:52 +0100 cpatel@elegosoft.com  [FIX][IMP] correction to unit tests, (issue#4516)
- 5780031a 2022-02-23 22:22:08 +0100 wagner@elegosoft.com  try to resolve unresolved conflicts from mass merge (issue #4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

