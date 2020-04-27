# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _


class ProductAppointment(models.Model):
    _name = 'product.appointment'
    _description = 'Appointment'

    name = fields.Char(
        'Name',
        required=True,
    )
    date_next_appointment = fields.Date(
        'Datum',
        required=True,
    )
    leads_of_notification = fields.Integer(
        'Leads of Notification',
        required=True,
    )
    time_interval = fields.Integer(
        'Time Inteval',
        required=True,
    )
    time_uom = fields.Selection(
        selection=[
            ('day', 'Day(s)'),
            ('month', 'Month(s)'),
        ],
        string='Time UoM',
        required=True,
        default="day",
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
            if record.date_next_appointment - relativedelta(
                days=record.leads_of_notification) == today:
                record.create_task = True

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
        if self.time_uom == 'day':
            self.date_next_appointment = today + relativedelta(days=self.time_interval)
        if self.time_uom == 'month':
            self.date_next_appointment = today + relativedelta(months=self.time_interval)

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

    @api.model
    def _cron_gen_update_appointment(self):
        all_appointments = self.search([])
        all_appointments.action_create_project_tasks()
