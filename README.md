[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat//12.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-vertical-rental-)
[![Build Status](https://travis-ci.com/OCA/vertical-rental.svg?branch=12.0)](https://travis-ci.com/OCA/vertical-rental)
[![codecov](https://codecov.io/gh/OCA/vertical-rental/branch/12.0/graph/badge.svg)](https://codecov.io/gh/OCA/vertical-rental)
[![Translation Status](https://translation.odoo-community.org/widgets/vertical-rental-12-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/vertical-rental-12-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Vertical Rental

This repo adds support for rental businesses to Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

This part will be replaced when running the oca-gen-addons-table script from OCA/maintainer-tools.

Stage of Elego Rental Vertical Odoo Modules for OCA

Currently we have these modules to support rental business:

* [rental_base (Rental Base)](rental_base/README.rst): Base module for rental use cases
* [rental_contract (Rental Contract)](rental_contract/README.rst): Extension of module contract for rental use cases
* [rental_contract_insurance (Rental Contract Insurance)](rental_contract_insurance/README.rst): Rental Contract Insurance
* [rental_contract_month (Rental Contract Month)](rental_contract_month/README.rst): Extension of module rental_contract and rental_pricelist
* [rental_contract_toll_collect (Rental Contract Toll Collect)](rental_contract_toll_collect/README.rst): Invoice toll charge lines to customers periodically by contract usage.
* [rental_forward_shipment_plan (Rental Forward Shipment Plan)](rental_forward_shipment_plan/README.rst): Rental Routing Shipment Plan
* [rental_loan (Rental Loan)](rental_loan/README.rst): Extension of module action_loan for rental use cases
* [rental_menu_crm (Rental Menu CRM)](rental_menu_crm/README.rst): Add CRM to the Rental Menu
* [rental_offday (Rental Off Day)](rental_offday/README.rst): Calculate off-days in rentals on daily basis
* [rental_pricelist (Rental Pricelist)](rental_pricelist/README.rst): Enables the user to define different rental prices with time uom ("Month", "Day" and "Hour").
* [rental_product_instance (Rental Product Instance)](rental_product_instance/README.rst): Add product instances identified by serial number as unique rented objects
* [rental_product_instance_appointment (Rental Product Instance Appointment)](rental_product_instance_appointment/README.rst): Rental Product Instance Appointment
* [rental_product_instance_repair (Rental Product Instance Repair)](rental_product_instance_repair/README.rst): Extension of module rental_product_instance and rental_repair
* [rental_product_insurance (Rental Product Insurance)](rental_product_insurance/README.rst): Sell Insurance of Product
* [rental_product_pack (Rental Product Pack)](rental_product_pack/README.rst): Allow use of product packs as in rental use cases
* [rental_product_set (Rental Product Set)](rental_product_set/README.rst): Extends the sale_product_set to add rented product set on sale order lines.
* [rental_product_variant (Rental Product Variant)](rental_product_variant/README.rst): Extends model product with several fields for rental use cases.
* [rental_purchase_order_type (Rental Purchase Order Type)](rental_purchase_order_type/README.rst): Additional purchase order types for rental use cases: transport orders and repair orders
* [rental_quality_control (Rental Quality Control)](rental_quality_control/README.rst): New text field to define the reason for quality failure.
* [rental_repair (Rental Repair)](rental_repair/README.rst): Support repair orders during rental periods
* [rental_reporting (Rental Reporting)](rental_reporting/README.rst): Add rental-specific reporting menu and functions
* [rental_routing (Sale Rental Routing)](rental_routing/README.rst): This module adds support for the management of transports of rental products.
* [rental_sale (Rental Sale)](rental_sale/README.rst): Manage Rental of Products
* [rental_timeline (Rental Timeline)](rental_timeline/README.rst): Adds a timeline to products as well as a timeline view as overview of all rental products and orders
* [rental_timeline_offday (Rental Timeline Offday)](rental_timeline_offday/README.rst): Extends the rental_timeline module to show the offday_number in the timeline popup.
* [rental_timeline_product_instance (Rental Timeline Product Instance)](rental_timeline_product_instance/README.rst): Extends the rental_timeline module to show the product instance fields in the timeline product popup.
* [rental_timeline_product_instance_appointment (Rental Timeline Product Instance Appointment)](rental_timeline_product_instance_appointment/README.rst): Extends the rental_timeline module to display an appointment icon in the mouse over if there is an appointment during the rental time.
* [rental_timeline_product_variant (Rental Timeline Product Variant)](rental_timeline_product_variant/README.rst): Extends the rental_timeline module to show the product variant fields in the timeline product popup.
* [rental_timeline_repair (Rental Timeline Repair)](rental_timeline_repair/README.rst): extends the rental_timeline module to show the repair orders in the timeline.
* [rental_timeline_transport (Rental Timeline Transport)](rental_timeline_transport/README.rst): extends the rental_timeline module to show the transport order fields in the timeline popup.
* [rental_toll_collect (Rental Toll Collect)](rental_toll_collect/README.rst): Import a CSV file from Toll Collect and invoice the costs to customers.
* [shipment_plan (Shipment Management)](shipment_plan/README.rst): Shipment Management
* [shipment_plan_rental (Shipment Plan Rental)](shipment_plan_rental/README.rst): Shipment Plan for Rental
* [shipment_plan_sale (Sale Shipment Plan)](shipment_plan_sale/README.rst): Sale Shipment Plan

The shipment_plan modules should probably be moved to OCA/stock-logistics-transport.

There is a presentation video at Youtube: https://www.youtube.com/watch?v=CzO5NqgJWD0

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to OCA
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
