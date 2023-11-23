Rental Product Variant
====================================================

*This file has been generated on 2023-02-19-14-21-34. Changes to it will be overwritten.*

Summary
-------

Extends model product with several fields for rental use cases.

Description
-----------

This module adds several fields to the product form.

Additional fields:
 - further_ref [Char]: additional reference
 - qr_code [Char]: QR code
 - manu_year [Char]: year of manufacture
 - manu_id [Many2one]: product.manufacturer -- manufacturer
 - manu_type_id [Many2one]: product.manufacturer.type -- type
 - fleet_type_id [Many2one]: fleet.type -- fleet type

 - rental_order_ids [One2many]: sale.rental -- rented_product_id -- Rental Orders
 - stock_move_ids [One2many]: stock.move -- product_id -- Stock Moves
 - additional_info [Html]: arbitrary additional infomation

Additional fields configured and added by product category:
 - Show Product Identification Number -> product_number [Char]: product identification number
 - Show Vehicle Identification Number -> vehicle_number [Char]: vehicle identification number
 - Show License Plate -> license_plate [Char]: license plate
 - Show Initial Registration -> init_regist [Date]: date of initial registration
