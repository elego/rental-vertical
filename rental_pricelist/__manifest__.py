# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Pricelist",
    "summary": 'Enables the user to define different rental prices with time uom ("Month", "Day" and "Hour").',
    "description": """
Rental prices are usually scaled prices based on a time unit, typically day, sometimes months or hour.
This modules integrates the standard Odoo pricelists into rental use cases and allows the user an
easy way to specify the prices in a product tab as well as to use all the enhanced pricelist features.
""",
    "usage": """
- Create a product and mark it as rentable by setting rental = True.
- Go to page 'Rental Price'.
- Activate the required boolean fields for hourly, daily or monthly rental.
- Save the product.
- Add a usual price for one hour, one day or one month.
- Add bulk prices, e.g. one day costs 300 €, 7 days 290 €, 21 days 250 €, and so on.

Hint: The bulk prices are added in the product form view of the stockable, rentable product 
but are actually used for its related rental service!
    """,
    "version": "12.0.1.0.1",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_base",
    ],
    "data": [
        "views/sale_view.xml",
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
