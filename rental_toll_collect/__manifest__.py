# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Toll Collect",
    "summary": "Import a CSV file from Toll Collect and invoice the costs to customers.",
    "version": "14.0.1.0.0",
    "category": "Rental",
    "author": "elego Software Solutions GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/vertical-rental",
    "description": """
This module provides the opportunity to import csv files downloaded from toll collect portal.
During import it matches the given license plate in csv file with a vehicle product.
The toll charge lines can be invoiced to a customer manually or by creating an invoice from a 
sale/rental order containing a vehicle product as sale/rental order line.

The csv should contain the following columns:

- Account number ("Mautaufstellungs-Nr.")
- license plate ("Kfz-Kennz.")
- Date ("Datum")
- Start ("Start")
- Booking number ("Buchungsnummer")
- Type ("Art")
- Route Ramp ("Auffahrt")
- Route Via ("über")
- Route Exit ("Abfahrt")
- Analytic Account ("Kostenstelle")
- Tariff Model ("Tarifmodell")
- Axle class ("Achsklasse")
- Weight class ("Gewichtsklasse")
- Polution class ("Schadstoffklasse")
- Road operator ("Straßenbetreiber")
- Procedure ("Verf.¹")
- Distance ("km")
- Amount ("EUR")
""",
    "depends": [
        "rental_base",
        "rental_product_instance",
        "rental_pricelist",
        "product_analytic",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product_data.xml",
        "data/report_paperformat.xml",
        "views/toll_charge_line_view.xml",
        "views/account_invoice_view.xml",
        "views/product_view.xml",
        "views/res_config_settings_view.xml",
        "views/res_partner_view.xml",
        "views/sale_view.xml",
        "wizard/toll_charge_line_import_view.xml",
        "wizard/toll_charge_line_invoicing_view.xml",
        "report/toll_collect_report.xml",
        "report/toll_report_templates.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": False,
    "installable": True,
    "license": "AGPL-3",
    "post_init_hook": "post_init_hook",
}
