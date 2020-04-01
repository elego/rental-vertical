# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Invoice',
    'summary': '''Rental Invoice''',
    'description': '''
This module add the 2-phase confirmation of incoming invoices including delegated charging to customers.

The accountant or purchaser has to confirm both the successful factual check,
i.e. the company expected to get this invoice, and the successful
arithmetical check, i.e. the product quantities, prices, accounts and taxes are correct.
If this incoming invoice should be invoiced to a customer, an outgoing invoice can be
created directly from the vendor bill and will have the same invoice lines.
''',
    'usage': '''
In order to manage this 2-phase confirmation process on incoming invoices, the user needs the following groups:
- 'Do factual check on incoming invoices'
- 'Do arithmetical check on incoming invoices'
- 'Create outgoing invoice from incoming invoice'

The workflow is considered as this:
- There is an incoming invoice with one or several products.
- The accountant does the factual check (success or failure).
- The accountant decides if an outgoing invoice is needed (boolean field).
- If the factual check was successful, the accountant does the arithmetical check (success or failure).
- If the arithmetical check was successful and an outgoing invoice is needed, the accountant creates it.
- If all checks are successful, the incoming invoice can be validated.
- Otherwise the incoming invoice cannot be validated.
''',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'Elego Software Solutions GmbH',
    'depends': [
        'account',
        'account_invoice_start_end_dates',
        'account_invoice_pricelist',
    ],
    'data': [
        'data/groups.xml',
        'wizard/create_forward_invoice_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'license': 'AGPL-3',
}
