# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Loan",
    "summary": "Extension of module action_loan for rental use cases",
    "description": """
This module adds a smartbutton to the product form view to get an overview of all loans 
(from module account_loan in repository account_financial_tools) that are linked to this 
specific product.
    """,
    "usage": """
- Install the module.
- Add a loan with is_leasing = True and link a product.
- Go to the product form view and see the smartbutton for loans.
    """,
    "version": "15.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "usage": """
This module is automatically installed when all of the following modules are installed in a database:

- account_loan
- rental_base
    """,
    "depends": [
        "account_loan",
        "rental_base",
        "rental_product_variant",
    ],
    "data": [
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
