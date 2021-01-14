# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Pricelist (Interval)",
    "summary": 'Enables the user to define different rental prices with time uom ("Month", "Day" and "Hour").',
    "description": """
This modules enable a special interval price system, that are base on daily rental pricelist.
""",
    "usage": """
- Create a product and mark it as rentable by setting rental = True.
- Go to page 'Rental Price'.
- Activate the required boolean fields for daily rental.
- Save the product.
- Add a usual price for one day
- Add Interval Price and pricelist items
- Set Max Days for interval Price

Example for price items:
::
Max Days for interval 21 days
min (days)     price
1                100
8                175
15               225

that means:
::
1  -  7 days for 100 EURO
8  - 14 days for 175 EURO
15 - 21 days for 225 EURO.

- Alternative you can define the rule in form view of company
- and click the button "reset interval prices" to create the price items automatically

Example for rules:
::
min (days)     factor
1                1
8                1.75
15               2.25
- Activate the interval price in sale order line (Use Interval Price)
    """,
    "version": "12.0.1.0.1",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_pricelist",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_view.xml",
        "views/product_view.xml",
        "views/res_company_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "application": False,
    "license": "AGPL-3",
}
