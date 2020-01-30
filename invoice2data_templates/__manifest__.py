# © 2015-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Invoice2data Templates",
    "version": "12.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "summary": "Manage invoice2data templates for invoice import",
    "author": "OCA, Elego Software Solutions GmbH",
    "website": "http://www.akretion.com",
    "depends": ["account_invoice_import_invoice2data"],
    "external_dependencies": {"python": ["invoice2data"]},
    "data": [
        "security/ir.model.access.csv",
        "security/rule.xml",
        "views/invoice2data_templates.xml"
    ],
    "demo": [
        "demo/demo_data.xml"
    ],
    "images": ["images/sshot-wizard1.png"],
    "installable": True,
}
