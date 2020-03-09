
Usage
-----

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

