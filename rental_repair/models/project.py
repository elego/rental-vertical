# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import math
from odoo import api, exceptions, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        domain="[('product_instance', '=', True)]",
    )

    partner_id = fields.Many2one(
        string="Partner",
    )

    tracking = fields.Selection(
        string="Tracking",
        related="product_id.tracking",
    )

    lot_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string="Serial Number",
    )

    repair_ids = fields.One2many(
        comodel_name="repair.order",
        inverse_name="project_task_id",
        string="Repair Orders",
        groups="stock.group_stock_user",
    )

    vendor_repair_ids = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="project_task_id",
        string="Vendor Repair Orders",
    )

    phone = fields.Char(
        string="Phone",
        help="Phone number",
    )

    mobile = fields.Char(
        string="Mobile",
        help="Mobile number",
    )

    stagnation_ids = fields.One2many(
        comodel_name="project.task.stagnation",
        inverse_name="project_task_id",
        string="Stagnation",
    )

    total_stagnation_time_sec = fields.Float(
        string="Total stagnation (seconds)",
        compute="_compute_stagnation_time",
    )

    total_stagnation_time = fields.Char(
        string="Total stagnation",
        compute="_compute_stagnation_time",
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        super(ProjectTask, self)._onchange_partner_id()
        self.phone = self.partner_id.phone
        self.mobile = self.partner_id.mobile

    def _seconds_to_human_readable(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        r = "{days} {day} {hours} {hour} {minutes} {minute} {seconds} {second}".format(
            days=_("{} days").format(d) if d > 1 else "",
            day=_("{} day").format(d) if d == 1 else "",
            hours=_("{} hours").format(h) if h > 1 else "",
            hour=_("{} hour").format(h) if h == 1 else "",
            minutes=_("{} minutes").format(m) if m > 1 else "",
            minute=_("{} minute").format(m) if m == 1 else "",
            seconds=_("{} seconds").format(s) if s > 1 else "",
            second=_("{} second").format(s) if s == 1 else "",
        )

        return " ".join(r.split())

    @api.depends("stagnation_ids.start_time", "stagnation_ids.end_time")
    def _compute_stagnation_time(self):
        for task in self:
            s = sum(
                [
                    math.ceil((i.end_time - i.start_time).total_seconds())
                    for i in task.stagnation_ids
                ]
            )
            task.total_stagnation_time_sec = s
            task.total_stagnation_time = (
                self._seconds_to_human_readable(s) if s > 0 else "-"
            )


class ProjectStagnation(models.Model):
    _name = "project.task.stagnation"
    _description = "Project task stagnation"

    sql_constraints = [
        (
            "check_datetime_range",
            "CHECK(end_time > start_time)",
            "The start time must be earlier than the end time.",
        ),
    ]

    project_task_id = fields.Many2one(
        comodel_name="project.task",
        string="Ticket",
        ondelete="set null",
    )

    start_time = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
        copy=False,
    )

    end_time = fields.Datetime(
        required=True,
        copy=False,
    )

    note = fields.Text()

    @api.constrains("start_time", "end_time")
    def check_datetime_range(self):
        for stagnation in self:
            if stagnation.end_time <= stagnation.start_time:
                msg = _(
                    "The start time '{start_time}' must be earlier than the end time {end_time}."
                ).format(
                    start_time=stagnation.start_time,
                    end_time=stagnation.end_time,
                )
                raise exceptions.UserError(msg)
