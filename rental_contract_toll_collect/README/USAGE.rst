
Usage
-----

- Create a rental order with vehicle products as rental order lines.
- The products needs to be rented out in months in order to automatically create the contract.
- Confirm the rental order and see the newly created contract.
- Import the csv-file downloaded from Toll Collect Portal in order to create toll charge lines.
- The cronjob will automatically create invoices for this contract.
- If the date of the imported toll charge lines match the service period of invoice lines to be created, 
a new invoice line with the toll product is additionally added for each vehicle product with distance and amount.

