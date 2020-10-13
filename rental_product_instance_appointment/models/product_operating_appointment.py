# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _


class ProductOperatingAppointment(models.Model):
    _name = 'product.operating.appointment'
    _description = 'Operating Appointment'
    _order = 'date_next_appointment desc'

    name = fields.Char(
        'Name',
        required=True,
    )
    date_next_appointment = fields.Date(
        'Date',
        compute="_compute_date_next_appointment",
    )
    date_last_appointment = fields.Date(
        'Last Date',
        related="last_task_id.date_deadline",
    )
    leads_of_notification = fields.Integer(
        'Leads of Notification',
        required=True,
    )
    threshold = fields.Integer(
        'Threshold',
    )
    interval = fields.Integer(
        'Interval',
        required=True,
    )
    daily_increase = fields.Integer(
        'Daily Increase',
        default=1,
    )
    operating_uom = fields.Selection(
        selection=[
            ('km', 'Kilometer'),
            ('hour', 'Operating Hours'),
        ],
        string='Operating UoM',
        related="product_id.show_instance_condition_type",
    )
    product_id = fields.Many2one(
        'product.product',
        string="Instance",
        domain=[('product_instance', '=', True)],
    )
    create_task = fields.Boolean(
        'Create Task',
        compute="_compute_create_task",
    )
    last_task_id = fields.Many2one(
        'project.task',
        string="Last Ticket",
    )

    @api.multi
    def _compute_create_task(self):
        today = fields.Date.from_string(fields.Date.today())
        for record in self:
            record.create_task = False
            if record.product_id.show_instance_condition_type not in ('km', 'hour'):
                continue
            date_notification = record.date_next_appointment - relativedelta(
                days=record.leads_of_notification
            ) 
            if date_notification == today \
                    or (date_notification < today and not record.date_last_appointment) \
                    or (date_notification < today and record.date_last_appointment < today):
                record.create_task = True

    @api.multi
    def _compute_date_next_appointment(self):
        for record in self:
            record._update_next_appointment()

    def _prepare_task_vals(self):
        self.ensure_one()
        helpdesk = self.env.ref('rental_repair.project_project_helpdesk')
        res = {
            'product_id': self.product_id.id,
            'lot_id': self.product_id.instance_serial_number_id.id,
            'date_deadline': self.date_next_appointment,
            'project_id': helpdesk.id,
            'name': "%s: %s" %(self.name, self.product_id.name),
        }
        return res

    def _update_next_appointment(self):
        self.ensure_one()
        today = fields.Date.from_string(fields.Date.today())
        diff = 0
        if self.operating_uom == 'km':
            km = self.product_id.instance_condition_km and float(self.product_id.instance_condition_km) or 0.0
            diff = self.threshold - km
        elif self.operating_uom == 'hour':
            hour = self.product_id.instance_condition_hour and float(self.product_id.instance_condition_hour) or 0.0
            diff = self.threshold - hour
        days = diff / self.daily_increase
        self.date_next_appointment = today + relativedelta(days=days)

    @api.multi
    def action_create_project_tasks(self):
        task_obj = self.env['project.task']
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
