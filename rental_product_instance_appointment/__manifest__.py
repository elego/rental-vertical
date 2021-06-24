# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Product Instance Appointment",
    "summary": "Rental Product Instance Appointment",
    "description": """
Product instances are unique products in a current state and some tasks needs to be regularly done with them.
This module provides the possibility to add single or recurrent appointments for a product which automatically
create project tasks a defined time before the actual appointment date.

You can distinguish between time dependent and usage dependent appointments.
Time dependent appointments are due on a specific date.
Usage dependent appointments are due if a specific condition is reached, 
like a certain mileage or amount of operating hours.
""",
    "usage": """
- Create a product instance.

- Add one or several time dependent appointments in 'Appointments' page on product view.
- Set a name, date, a notification lead time (in days) and a time interval for each appointment.
- Before the appointment is due a project task will be created automatically by a cronjob using the lead time.
- If the appointment date is today, the next appointment is calculated by the intervall.

- Add one or several usage dependent appointments in 'Appointments' page on product view.
  The product instance therefore need a condition type configured by its product category.
- Set a name, a threshold, an intervall, a notification lead time (in days) and a daily increase.
- If there are no existing operating data yet, the daily increase is by default 1 and the appointment 
  date is calculated using 'today' as a reference until the threshold is reached.
- If there are operating data, the daily increase is calculated from the value and date difference, 
  using the last 20 operating data that differ in value and time.
- A project task is automatically created before the calculated appointment date using the lead time.
""",
    "version": "12.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_product_instance_repair",
        "project_stage_closed",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/product_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "auto_install": False,
    "license": "AGPL-3",
}
