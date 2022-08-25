# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Contract",
    "summary": "Extension of module contract for rental use cases",
    "description": """
During longtime rentals, it is often required to write invoices in regular intervals.
This is possible with the contract module, which is here extended to support rental
use cases in extension to purchase and sale use cases.

The module adds subtypes for contracts in order to distinguish between customer contracts, 
customer rental contracts, vendor contracts and vendor rental contracts. 
It is possible to add more subtypes with own sequence, which automatically sets the contract's code.

- If a contract is automatically created from sale order, it passes the sale order type to the contract subtype.
- The analytic account of a product is automatically set on the contract line.
- The start and end date of invoice lines are automatically set when creating the invoice from a contract.
- Both fields date_start and date_end that are used for contract lines are now hidden and related to the given 
  start and end date of sale order line.
""",
    "usage": """
You can add new contract subtypes here:

 - Invoicing > Configuration > Contract > Contract Subtypes
 - Rentals > Configuration > Contract > Contract Subtypes
 
 - Create a sale order.
 - Choose a sale type.
 - Add a rental product that has a rental service marked as contract with a contract template 
   and an analytic income account.
 - Choose a service period by setting start and end date.
 - Confirm the order.
 - Check the automatically created contract for contract type, analytic accounts, ...

This module is automatically installed when all of the following modules are installed in a database:

 - contract
 - product_contract
 - sale_start_end_dates
 - sale_rental
 - rental_base
""",
    "version": "14.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "contract",
        "product_contract",
        "product_analytic",
        "sale_start_end_dates",
        "sale_rental",
        "rental_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/default_type_data.xml",
        "data/contract_template_data.xml",
        "views/contract_view.xml",
        "views/sale_view.xml",
        "views/product_view.xml",
        "views/contract_order_type_view.xml",
        "views/res_partner_view.xml",
        "views/account_invoice_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": True,
    "license": "AGPL-3",
}
