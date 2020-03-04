# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Product Variant',
    'summary': 'Extends model product with several fields for rental use cases.',
    'description': '''
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
''',
    'version': '12.0.1.0.0',
    'category': 'product',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}
