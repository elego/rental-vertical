# Part of rental-vertical See LICENSE file for full copyright and licensing details.

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
    'author': 'Elego Software Solutions Gmbh',
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
    'license': 'LGPL-3',
}
