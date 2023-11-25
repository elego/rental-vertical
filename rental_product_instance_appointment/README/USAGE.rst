
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
