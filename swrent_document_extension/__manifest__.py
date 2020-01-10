# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Document Extension',
    'summary': '''
This module enable the user to use following actions of the documents

1. assign the document to a record
2. create a draft invoice
3. import vendor bills
4. validate the document
5. assign the documents to a system user

''',
    'version': '12.0.1.0.0',
    'category': 'document',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'depends': [
        'stock',
        'sale',
        'purchase',
        'account',
        'knowledge',
        'document',
        'account_invoice_import_invoice2data',
        'account_invoice_import_ubl',
        'account_invoice_import_docs',
        'account_invoice_import_factur-x',
    ],
    'data': [
        'wizard/assign_document_view.xml',
        'views/ir_attachment_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
