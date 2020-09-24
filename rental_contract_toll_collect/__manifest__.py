# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract Toll Collect',
    'summary': "Invoice toll charge lines to customers periodically by contract usage.",
    'description': """
This module is an extension of rental_toll_collect. When using contracts for periodic 
invoicing of rental orders, this module provides the opportunity to also invoice the 
toll charges for the given time period.
    """,
    'usage': """
- Create a rental order with vehicle products as rental order lines.
- The products needs to be rented out in months in order to automatically create the contract.
- Confirm the rental order and see the newly created contract.
- Import the csv-file downloaded from Toll Collect Portal in order to create toll charge lines.
- The cronjob will automatically create invoices for this contract.
- If the date of the imported toll charge lines match the service period of invoice lines to be created, 
  a new invoice line with the toll product is additionally added for each vehicle product with distance and amount.
    """,
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA) / elego Software Solutions GmbH',
    'depends': [
        'rental_toll_collect',
        'rental_contract_month',
    ],
    'data': [
        'views/contract_views.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'AGPL-3',
}
