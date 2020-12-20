# Copyright 2014-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016-2019 Sodexis (http://sodexis.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Rental Sale",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "license": "AGPL-3",
    "summary": "Manage Rental of Products",
    "description": """
With this module, you can rent products with Odoo. This module supports:

- regular rentals.
- rental extensions.
- sale of rented products.

""",
    "configuration": """
In the menu *Sales > Products > Product Variants*, on the form view of a stockable product or consumable, in the *Rental* tab, there is a button *Create Rental Service* which starts a wizard to generate the corresponding rental service.

In the menu *Warehouse > Configuration > Warehouses*, on the form view of the warehouse, in the *Technical Information* tab, you will see two additional stock locations: *Rental In* (stock of products to rent) and *Rental Out* (products currently rented). In the *Warehouse Configuration* tab, make sure that the option *Rental Allowed* is checked.

To use the module, you need to have access to the form view of sale order lines. For that, you must add your user to one of these groups:

- Manage Product Packaging
- Properties on lines

Upon module installation, all users are automatically added to the group *Manage Product Packaging*.

""",
    "usage": """
In a sale order line (form view, not tree view), if you select a rental service, you can :

- create a new rental with a start date and an end date: when the sale order is confirmed, it will generate a delivery order and an incoming shipment.
- extend an existing rental: the incoming shipment will be postponed to the end date of the extension.

In a sale order line, if you select a product that has a corresponding rental service, you can decide to sell the rented product that the customer already has. If the sale order is confirmed, the incoming shipment will be cancelled and a new delivery order will be created with a stock move from *Rental Out* to *Customers*.

Please refer to this screencast https://www.youtube.com/watch?v=9o0QrGryBn8 to get a demo of the installation, configuration and use of this module (note that this screencast is for Odoo v7).


""",
    "author": "Akretion, Sodexis, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": ["sale_start_end_dates", "sale_stock", "sales_team"],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_rental_security.xml",
        "data/res_config_settings_data.xml",
        "data/rental_data.xml",
        "views/sale_order.xml",
        "views/stock_warehouse.xml",
        "views/sale_rental.xml",
        "wizard/create_rental_product_view.xml",
        "views/product.xml",
    ],
    "post_init_hook": "add_to_group_stock_packaging",
    "demo": ["demo/rental_demo.xml"],
    "installable": True,
}
