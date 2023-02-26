Rental Toll Collect
====================================================

*This file has been generated on 2023-02-19-14-17-56. Changes to it will be overwritten.*

Summary
-------

Import a CSV file from Toll Collect and invoice the costs to customers.

Description
-----------

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


Usage
-----

-  Go to Rentals > Configuration > Settings
- Activate the automatic invoicing of toll charges if toll charges should be automatically invoiced together with rental services.
- Create a rental order with vehicle products as rental order lines.
- Confirm the rental order.
- Go to Rentals > Product > Toll Charges > Import Toll Charges.
- Upload your csv file and import the file.
- Go to Rentals > Product > Toll Charges > Toll Charge Lines and see all imported toll charge lines.
- Go to a vehicle product and click on smartbutton for toll charges and see all related toll charge lines.
- Go back to the rental order and create an invoice.
- If the date of the toll charge lines match the service period of rental order lines,
  a new invoice line is additionally added for each vehicle product with distance and amount.

- Mark one or several toll charge lines in tree view and create an invoice via action wizard to invoice them manually.

Changelog
---------

- c92a1b33 2022-05-04 12:54:10 +0200 wagner@elegosoft.com  update doc (issue #3613, issue #4016)
- 19e327a4 2022-04-18 14:45:33 +0000 jenkins-ci@elegosoft.com  add new rental logo and update doc (issue #3613, issue #4016)
- 8d191ff7 2022-04-10 15:41:16 +0200 wagner@elegosoft.com  add missing/lost documentation (issue #4516)
- fb3a6bbf 2022-03-17 09:43:02 +0100 cpatel@elegosoft.com  [IMP] toll_collect_tour correction/migration, (issue#4516)
- 279539a5 2022-03-14 10:48:31 +0100 cpatel@elegosoft.com  [IMP] correction,migration,fix unit test errors, (issue#4516)
- b5dd7aac 2022-03-01 13:56:52 +0100 cpatel@elegosoft.com  [FIX][IMP] correction to unit tests, (issue#4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

