Rental Contract
====================================================

*This file has been generated on 2022-05-04-12-21-41. Changes to it will be overwritten.*

Summary
-------

Extension of module contract for rental use cases

Description
-----------

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

