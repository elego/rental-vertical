
Changelog
---------

- 977d224 [IMP] todo points issue # 3279
- e371276 [MERGE] remotes/origin/fix_3339_blp343_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp343_extend_documentation_v12 - 9576b54fbb0cbcbffb804587fd722df8a4057da0 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- eae607f [MERGE] remotes/origin/feature_3279_blp343_todo_points_v12: addons-rental-vertical remotes/origin/feature_3279_blp343_todo_points_v12 - 290795012d9932bfc08060449d3386c2fbcd7483 [IMP] todo points    1. move 'additional info' page behind 'general info' (so it is the second tab)    3. fix the order of smartbuttons       remove 'on hand' smartbutton if product ist product instance       remove 'forecastes' smartbutton if product ist product instance       remove 'routes' smartbutton if product ist product instance       remove 'purchased' smartbutton if product ist product instance       remove 'sold' smartbutton if product ist product instance    4. fix exception after clicking on smartbutton 'sale orders'       ValueError: External ID not found in the system: rental_base.action_normal_orders    5. fix problem that the invoice form view cannot be opend after clicking on smartbutton 'invoices'
- 9576b54 allow cli overwrite of module arguments; regenerate doc for rental_product_instance_appointment rental_product_variant rental_offday rental_invoice rental_contract_month rental_contract (issue #3339)
- 9ae7b8d issue #3279 add submenu for product config in rental menu
- e030fd1 issue #3279 add description and usage section for rental_product_variant
- 2907950 [IMP] todo points    1. move 'additional info' page behind 'general info' (so it is the second tab)    3. fix the order of smartbuttons       remove 'on hand' smartbutton if product ist product instance       remove 'forecastes' smartbutton if product ist product instance       remove 'routes' smartbutton if product ist product instance       remove 'purchased' smartbutton if product ist product instance       remove 'sold' smartbutton if product ist product instance    4. fix exception after clicking on smartbutton 'sale orders'       ValueError: External ID not found in the system: rental_base.action_normal_orders    5. fix problem that the invoice form view cannot be opend after clicking on smartbutton 'invoices'
- 804dc44 regenerate module documentation (issue #3339)
- 4c76ef2 [MERGE] remotes/origin/fix_3339_blp311_extend_documentation_v12: addons-rental-vertical remotes/origin/fix_3339_blp311_extend_documentation_v12 - 7dde7fa1ec109919795e59198feb24fc96fcfeb1 add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- bf364e7 add some fields to the search view; issue #3296
- 7dde7fa add changelogs in HISTORY.rst and some minor improvements (issue #3339)
- 467665c add some generated reST and HTML documentation (issue #3339)
- 6965ed1 fix some mistakes in author and license, make summaries one line, add some descriptions (issue #3339)
- 41ec0c4 [IMP] redefine fields for instance current condition
- 4d17de4 [IMP] adjusts smartbuttons of product variant
- a88dfb5 [IMP] refactoring of menus
- d3c07ec issue #3279 add German translation for rental_product_variant
- 41fb557 [FIX] fixes timeline view errors
- bbcea0f [FIX] fixes error by copying a product variant
- 2f11b55 [IMP] improves form view of products
- b5f3dbc [IMP] fixes errors in module rental_product_pack and redefine type of field 'init_regist' Char -> Date
- 94e76bb [IMP] set liscense, copyrights and author
- b2e6d5c [IMP] Add neu Module rental_base, rental_product_pack and Refactoring of module sale_rental_menu (deprecated)
- 676c70b [IMP] Refactoring of module swrent_product_extension

