Rental Sale
====================================================

*This file has been generated on 2020-10-28-20-56-22. Changes to it will be overwritten.*

Summary
-------

Manage Rental of Products

Description
-----------

With this module, you can rent products with Odoo. This module supports:

- regular rentals.
- rental extensions.
- sale of rented products.


Configuration
-------------

In the menu *Sales > Products > Product Variants*, on the form view of a stockable product or consumable, in the *Rental* tab, there is a button *Create Rental Service* which starts a wizard to generate the corresponding rental service.

In the menu *Warehouse > Configuration > Warehouses*, on the form view of the warehouse, in the *Technical Information* tab, you will see two additional stock locations: *Rental In* (stock of products to rent) and *Rental Out* (products currently rented). In the *Warehouse Configuration* tab, make sure that the option *Rental Allowed* is checked.

To use the module, you need to have access to the form view of sale order lines. For that, you must add your user to one of these groups:

- Manage Product Packaging
- Properties on lines

Upon module installation, all users are automatically added to the group *Manage Product Packaging*.


Usage
-----

In a sale order line (form view, not tree view), if you select a rental service, you can :

- create a new rental with a start date and an end date: when the sale order is confirmed, it will generate a delivery order and an incoming shipment.
- extend an existing rental: the incoming shipment will be postponed to the end date of the extension.

In a sale order line, if you select a product that has a corresponding rental service, you can decide to sell the rented product that the customer already has. If the sale order is confirmed, the incoming shipment will be cancelled and a new delivery order will be created with a stock move from *Rental Out* to *Customers*.

Please refer to this screencast https://www.youtube.com/watch?v=9o0QrGryBn8 to get a demo of the installation, configuration and use of this module (note that this screencast is for Odoo v7).


Changelog
---------

- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  (HEAD -> v12, origin/v12) add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 6b7864e 2020-09-15 12:00:21 +0200 yweng@elegosoft.com  [IMP] Rename Module sale_rental to rental_sale

