
Changelog
---------

- d638ed9 2021-05-20 18:20:51 +0000 jenkins-ci@elegosoft.com  [MERGE] remotes/origin/fix_4168_blp1050_rename_sale_rental_v12: addons-rental-vertical remotes/origin/fix_4168_blp1050_rename_sale_rental_v12 - db62236826dd7f75e7bdb5b2a345d049102e145c [IMP] improves function _run_rental_procurement of sale.order.line (issue 4168)
- 1abc79f 2021-05-12 18:08:04 +0200 yweng@elegosoft.com  (origin/wip_4168_sale_rental_v12, wip_4168_sale_rental_v12) [IMP] adjust dependence of rental modules: replace rental_sale with sale_rental
- db62236 2021-04-01 15:19:32 +0200 yweng@elegosoft.com  (origin/fix_4168_blp1050_rename_sale_rental_v12) [IMP] improves function _run_rental_procurement of sale.order.line (issue 4168)
- bbd5cb2 2021-01-14 13:55:22 +0100 wagner@elegosoft.com  adapt gen-doc and update (issue #3613)
- 83ed8f7 2020-12-22 18:06:08 +0100 wagner@elegosoft.com  all Python code reformatted by black code formatter (issue #4016)
- ed7dc16 2020-12-04 13:52:03 +0100 yweng@elegosoft.com  (origin/fix_3975_blp862_rental_routing_v12) [FIX] property_stock_customer of res.partner
- c7e3b59 2020-11-06 09:59:46 +0100 wagner@elegosoft.com  regenerate doc from manifests (issue #3613)
- 391ef2a 2020-10-28 20:59:58 +0100 wagner@elegosoft.com  add usage information for product sets and product packs; add configuration and usage information for rental_sale and extend gen-doc for configuration (issue #3613)
- d39f57e 2020-10-28 20:18:47 +0100 wagner@elegosoft.com  add links to the index in README.md (issue #3613)
- b1039c8 2020-10-28 17:39:27 +0100 wagner@elegosoft.com  add index generation and add index to README.md (issue #3613)
- 363cb50 2020-10-28 16:59:43 +0100 wagner@elegosoft.com  change quotes in manifests of rental_forward_shipment_plan and rental_routing and add some draft information about routing; regenerate (issue #3613)
- 1be4b54 2020-09-15 12:08:18 +0200 yweng@elegosoft.com  (origin/feature_3866_blp804_rename_sale_rental_v12) [MIG] Rename Module sale_rental and rental_sale (update dependence and xml_id)
- 63e22e6 2020-09-10 14:38:42 +0200 yweng@elegosoft.com  (origin/fix_3856_blp778_duplicated_in_pickings_of_reconfirmed_sale_order_v12) [FIX] (#3856) the canceled pickings or moves of a canceled sale order should not be set into state 'confirmed' again, if the user confirm the canceled sale order again. It works with FIX feature_3856_blp778_rockbird_terminate_contract_v12 together
- 623403c 2020-08-18 14:17:31 +0200 yweng@elegosoft.com  (origin/defect_3851_blp740_rental_routing_v12) [FIX] do not use rental_onsite_location as property_stock_customer for res.partner
- c360524 2020-07-21 11:59:36 +0200 yweng@elegosoft.com  (origin/feature_3779_blp707_partner_rental_location_v12) [IMP] Create Rental Location and Rental Route by using display_name of the shipment address
- 4ad31ac 2020-06-26 12:56:43 +0200 yweng@elegosoft.com  (origin/defect_3729_blp666_sell_service_in_rental_order_v12) [IMP] add _description for model sale.rental.route.out.line, sale.rental.route.in.line and sale.rental.route
- cd86d15 2020-05-27 11:45:49 +0200 yweng@elegosoft.com  (origin/fix_3670_blp623_rental_end_date_v12) [FIX] fixes end_date of return move of rental
- 89adaaf 2020-05-16 14:54:03 +0200 wagner@elegosoft.com  fixup categories and regenerate documentation (issue #3339)
- 6052842 2020-05-06 20:53:44 +0200 yweng@elegosoft.com  (origin/feature_3432_blp543_forward_shipment_plan_v12) [IMP] use picking type 'internal' for forward transfer and add field 'dangerous_goods' for sale.order.line and shipment.plan
- 134218b 2020-05-03 18:34:51 +0200 wagner@elegosoft.com  (origin/feature_3339_blp541_update_doc_v12, feature_3339_blp541_update_doc_v12) unify license and author and regenerate documentation (issue #3613, issue #3339)
- 53e283d 2020-04-29 16:19:43 +0200 yweng@elegosoft.com  [IMP] Delete missing field ordered_qty in rental_routing
- 98f8e8e 2020-04-28 18:28:53 +0200 yweng@elegosoft.com  [FIX] action_confirm of sale.order
- f1fa9d3 2020-03-09 19:17:31 +0100 yweng@elegosoft.com  (origin/feature_3432_blp343_rental_routing_v12) [IMP] forward rental
- f160629 2020-03-09 16:55:43 +0100 yweng@elegosoft.com  [RENAME] module sale_rental_routing -> rental_routing

