# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _


class ProductOperatingAppointment(models.Model):
    _name = "product.operating.appointment"
    _description = "Operating Appointment"
    _order = "date_next_appointment desc"

    name = fields.Char(
        string="Name",
        required=True,
    )

    date_next_appointment = fields.Date(
        string="Date",
        help="This is the planned appointment date "
        "for this usage dependent appointment. "
        "It is computed by the difference of "
        "threshold and current operating data "
        "divided by the daily increase.",
        compute="_compute_date_next_appointment",
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

    threshold = fields.Integer(
        string="Threshold",
        help="This is the threshold value that has be "
        "reached to make the appointment necessary "
        "and thereby to create the task in the "
        "helpdesk project. This value is automatically "
        "incremented by the interval value as soon as "
        "a project task is created for the current threshold.",
    )

    interval = fields.Integer(
        string="Interval",
        help="This is the interval which defines the "
        "repetition of this appointment. As soon "
        "as the current appointment threshold is "
        "reached, the threshold is incremented by "
        "this interval.",
        required=True,
    )

    daily_increase = fields.Integer(
        string="Daily Increase",
        help="This is the value that defines how the "
        "operating data are increased day by day. "
        "The default value is 1 but is automatically "
        "updated and computed after adding new "
        "operating data.",
        default=1,
    )

    operating_uom = fields.Selection(
        string="Operating UoM",
        related="product_id.show_instance_condition_type",
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
            if record.product_id.show_instance_condition_type not in ("km", "hour"):
                continue
            date_notification = record.date_next_appointment - relativedelta(
                days=record.leads_of_notification
            )
            if (
                date_notification == today
                or (date_notification < today and not record.date_last_appointment)
                or (date_notification < today and record.date_last_appointment < today)
            ):
                record.create_task = True

    def _compute_date_next_appointment(self):
        for record in self:
            record._update_next_appointment()

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
        diff = 0
        if self.operating_uom == "km":
            km = (
                self.product_id.instance_condition_km
                and float(self.product_id.instance_condition_km)
                or 0.0
            )
            diff = self.threshold - km
        elif self.operating_uom == "hour":
            hour = (
                self.product_id.instance_condition_hour
                and float(self.product_id.instance_condition_hour)
                or 0.0
            )
            diff = self.threshold - hour
        increase = self.daily_increase if self.daily_increase != 0 else 1
        days = diff / increase
        origin_date = (
            self.product_id.instance_condition_date.date()
            if self.product_id.instance_condition_date
            else today
        )
        self.date_next_appointment = origin_date + relativedelta(days=days)

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
                record.threshold += record.interval

    @api.model
    def _cron_gen_update_appointment(self):
        all_appointments = self.search([])
        all_appointments.action_create_project_tasks()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.product_id.update_operating_data_daily_increase()
        return res
