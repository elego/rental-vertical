# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductAppointment(models.Model):
    _name = "product.appointment"
    _description = "Appointment"
    _order = "date_next_appointment desc"

    name = fields.Char(
        string="Name",
        required=True,
    )

    date_next_appointment = fields.Date(
        string="Date",
        help="This is the appointment date " "for this time dependent appointment.",
        required=True,
    )

    date_last_appointment = fields.Date(
        string="Last Appointment Date",
        related="last_task_id.date_deadline",
    )

    last_appointment_stage_id = fields.Many2one(
        "project.task.type",
        string="Last Appointment Stage",
        related="last_task_id.stage_id",
        store=True,
    )

    last_appointment_closed = fields.Boolean(
        string="Last Appointment Closed",
        related="last_appointment_stage_id.is_closed",
        store=True,
    )

    leads_of_notification = fields.Integer(
        string="Leads of Notification",
        help="This is the number of days previous "
        "to the appointment date in order to "
        "create a task in the helpdesk project "
        "as notfication. The deadline of this "
        "task is set to appointment date.",
        required=True,
    )

    time_interval = fields.Integer(
        string="Time Interval",
        help="This is the interval which defines the "
        "repetition of this appointment. Be aware "
        "of the used unit of measure.",
        required=True,
    )

    time_uom = fields.Selection(
        selection=[
            ("day", "Day(s)"),
            ("month", "Month(s)"),
        ],
        string="Time UoM",
        required=True,
        default="day",
    )

    product_id = fields.Many2one(
        "product.product",
        string="Instance",
        domain=[("product_instance", "=", True)],
    )

    create_task = fields.Boolean(
        string="Create Task",
        compute="_compute_create_task",
    )

    last_task_id = fields.Many2one(
        "project.task",
        string="Last Ticket",
        help="This is last created task in the "
        "helpdesk project related to this "
        "appointment.",
    )

    def _compute_create_task(self):
        today = fields.Date.from_string(fields.Date.today())
        for record in self:
            record.create_task = False
            if (
                record.date_next_appointment
                - relativedelta(days=record.leads_of_notification)
                == today
            ):
                record.create_task = True

    def _prepare_task_vals(self):
        self.ensure_one()
        helpdesk = self.env.ref("rental_repair.project_project_helpdesk")
        res = {
            "product_id": self.product_id.id,
            "lot_id": self.product_id.instance_serial_number_id.id,
            "date_deadline": self.date_next_appointment,
            "project_id": helpdesk.id,
            "name": "%s: %s" % (self.name, self.product_id.name),
        }
        return res

    def _update_next_appointment(self):
        self.ensure_one()
        today = fields.Date.from_string(fields.Date.today())
        if self.time_uom == "day":
            self.date_next_appointment = today + relativedelta(days=self.time_interval)
        if self.time_uom == "month":
            self.date_next_appointment = today + relativedelta(
                months=self.time_interval
            )

    def action_create_project_tasks(self):
        task_obj = self.env["project.task"]
        today = fields.Date.from_string(fields.Date.today())
        for record in self:
            if record.create_task:
                vals = record._prepare_task_vals()
                new_task = task_obj.create(vals)
                record.last_task_id = new_task
            if record.date_next_appointment == today:
                record._update_next_appointment()

    @api.model
    def _cron_gen_update_appointment(self):
        all_appointments = self.search([])
        all_appointments.action_create_project_tasks()
