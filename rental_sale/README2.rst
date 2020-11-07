Rental Sale
====================================================

*This file has been generated on 2020-11-06-09-57-10. Changes to it will be overwritten.*

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

- f3ca50c 2020-10-29 16:59:48 +0100 wagner@elegosoft.com  add old history of renamed sale_rental (issue #3613)
- 391ef2a 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- fb94de5 2020-10-28 16:20:59 +0100 wagner@elegosoft.com  add descriptions to rental_timeline modules and regenerate (issue #3613)
- f1affe5 2020-10-28 12:45:28 +0100 wagner@elegosoft.com  regenerate doc (issue #3613)
- 5244748 2020-10-27 14:52:26 +0100 wagner@elegosoft.com  regenerate documentation and add README.rst files (issue #3339)
- d02ea5d 2020-10-27 14:41:06 +0100 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-849) update doc generation script (issue #3339)
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 6b7864e 2020-09-15 12:00:21 +0200 yweng@elegosoft.com  [IMP] Rename Module sale_rental to rental_sale
- 6b7864e 2020-09-15 12:00:21 +0200 yweng@elegosoft.com  [IMP] Rename Module sale_rental to rental_sale
- c03f9c2 2020-09-15 11:51:00 +0200 yweng@elegosoft.com  [IMP] Rename Module sale_rental to rental_sale (i18n)
- 94dc79c 2020-05-16 18:10:44 +0200 wagner@elegosoft.com  (origin/fix_3339_blp559_extend_documentation_v12, fix_3339_blp559_extend_documentation_v12) update module documentation (issue #3339)
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 795b1b6 2020-04-24 20:58:26 +0200 wagner@elegosoft.com  (tag: bp_rental_v12_integration-cep-521, tag: bp_rental_v12_integration-cep-520, tag: bp_rental_v12_integration-cep-519, tag: bp_rental_v12_integration-cep-518, tag: bp_rental_v12_integration-cep-517, tag: bp_rental_v12_integration-cep-516, tag: bp_rental_v12_integration-cep-514, tag: bp_rental_v12_integration-cep-513, tag: bp_rental_v12_integration-cep-512, tag: bp_rental_v12_integration-cep-511, tag: bp_rental_v12_integration-cep-510, tag: bp_rental_v12_integration-cep-509, tag: bp_rental_v12_integration-cep-508, tag: bp_rental_v12_integration-cep-507, tag: bp_rental_v12_integration-cep-506, tag: bp_rental_v12_integration-cep-505, tag: bp_humanilog_v12_integration-cep-322, tag: bp_humanilog_v12_integration-cep-321, tag: bp_humanilog_v12_integration-cep-320, tag: baseline_rental-vertical_v12_swrent_daily_build-503, origin/rental_v12_integration-cep-503, rental_v12_integration-cep-503) regenerate documentation (issue #3613)
- 7fac932 2020-04-13 14:13:09 +0200 wagner@elegosoft.com  (origin/fix_3339_blp455_extend_documentation_v12, fix_3339_blp455_extend_documentation_v12) regenerate documentation (issue #3339)
- 6d3410b 2020-04-13 13:28:20 +0200 wagner@elegosoft.com  regenerate documentation (issue #3339)
- 0bab92d 2020-04-09 12:41:12 +0200 wagner@elegosoft.com  (origin/fix_3339_blp355_extend_documentation_v12, fix_3339_blp355_extend_documentation_v12) update/regenerate addon documentation (issue #3339)
- b49c01d 2020-03-15 10:12:53 +0100 wagner@elegosoft.com  (origin/fix_3339_blp384_extend_documentation_v12) regenerate doc (issue #3339)
- cea0e94 2020-03-13 20:38:19 +0100 wagner@elegosoft.com  update documentation to build 380 (issue #3339)
- 804dc44 2020-03-07 21:06:12 +0100 wagner@elegosoft.com  regenerate module documentation (issue #3339)
- 7dde7fa 2020-03-03 00:19:35 +0100 wagner@elegosoft.com  (origin/fix_3339_blp311_extend_documentation_v12, fix_3339_blp311_extend_documentation_v12) add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c 2020-03-01 15:50:45 +0100 wagner@elegosoft.com  (origin/feature_3339_blp297_add_some_module_descriptions_v12, feature_3339_blp297_add_some_module_descriptions_v12) add some generated reST and HTML documentation (issue #3339)
- a6cbee8 2020-02-19 12:33:40 +0100 yweng@elegosoft.com  [ADD] module rental_transit_route
- 775a974 2020-02-19 12:33:03 +0100 yweng@elegosoft.com  [ADD] module sale_rental

