Rental Product Variant
===========================================

*This file has been generated on 2020-03-03-00-17-55. Changes to it will be overwritten.*

Summary
-------

Extends model product with several fields for rental use cases.

Description
-----------

Configuration options:
 - Show Vehicle Identification Number
 - Show License Plate
 - Show Initial Registration

Additional fields:
    further_ref [Char]: additional reference
    qr_code [Char]: QR code
    manu_year [Char]: year of manufacture
    manu_id [Many2one]: product.manufacturer -- manufacturer
    manu_type_id [Many2one]: product.manufacturer.type -- type
    fleet_type_id [Many2one]: fleet.type -- fleet type

    vehicle_number [Char]: vehicle identification number
    license_plate [Char]: license plate
    init_regist [Date]: date of initial registration

    rental_order_ids [One2many]: sale.rental -- rented_product_id -- Rental Orders
    stock_move_ids [One2many]: stock.move -- product_id -- Stock Moves
    additional_info [Html]: arbitrary additional infomation
    dimension [Char]: dimension

