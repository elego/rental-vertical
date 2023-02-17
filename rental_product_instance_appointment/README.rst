Rental Product Instance Appointment
====================================================

*This file has been generated on 2022-04-10-15-34-31. Changes to it will be overwritten.*

Summary
-------

Rental Product Instance Appointment

Description
-----------

Product instances are unique products in a current state and some tasks needs to be regularly done with them.
This module provides the possibility to add single or recurrent appointments for a product which automatically
create project tasks a defined time before the actual appointment date.

You can distinguish between time dependent and usage dependent appointments.
Time dependent appointments are due on a specific date.
Usage dependent appointments are due if a specific condition is reached, 
like a certain mileage or amount of operating hours.


Usage
-----

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


Changelog
---------

- 279539a5 2022-03-14 10:48:31 +0100 cpatel@elegosoft.com  [IMP] correction,migration,fix unit test errors, (issue#4516)
- 4509f78a 2022-02-23 20:48:33 +0100 wagner@elegosoft.com  (origin/feature_4516_add_files_ported_from_v12_v14, feature_4516_add_files_ported_from_v12_v14) add files ported to v14 by cpatel and khanhbui (issue #4516)

