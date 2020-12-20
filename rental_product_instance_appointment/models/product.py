# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    appointment_ids = fields.One2many(
        "product.appointment",
        "product_id",
        string="Appointments",
    )

    operating_appointment_ids = fields.One2many(
        "product.operating.appointment",
        "product_id",
        string="Operating Appointments",
    )

    instance_next_service_date = fields.Date(
        compute="_compute_instance_next_service_date"
    )

    def _compute_instance_next_service_date(self):
        today = fields.Date.from_string(fields.Date.today())
        for rec in self:
            instance_next_service_date = False
            for app in rec.appointment_ids:
                # If a project task is created for this appointment,
                # the next appointment date would have been updated already
                if app.date_last_appointment:
                    if today <= app.date_last_appointment and (
                        not instance_next_service_date
                        or (
                            instance_next_service_date
                            and app.date_last_appointment < instance_next_service_date
                        )
                    ):
                        instance_next_service_date = app.date_last_appointment
                else:
                    if today <= app.date_next_appointment and (
                        not instance_next_service_date
                        or (
                            instance_next_service_date
                            and app.date_next_appointment < instance_next_service_date
                        )
                    ):
                        instance_next_service_date = app.date_next_appointment
            for app in rec.operating_appointment_ids:
                # If a project task is created for this appointment,
                # the next appointment date would have been updated already
                if app.date_last_appointment:
                    if today <= app.date_last_appointment and (
                        not instance_next_service_date
                        or (
                            instance_next_service_date
                            and app.date_last_appointment < instance_next_service_date
                        )
                    ):
                        instance_next_service_date = app.date_last_appointment
                else:
                    if today <= app.date_next_appointment and (
                        not instance_next_service_date
                        or (
                            instance_next_service_date
                            and app.date_next_appointment < instance_next_service_date
                        )
                    ):
                        instance_next_service_date = app.date_next_appointment
            if instance_next_service_date:
                rec.instance_next_service_date = instance_next_service_date

    @api.multi
    def update_operating_data_daily_increase(self):
        for product in self:
            if product.operating_appointment_ids:
                i = 20  # take last 20 operating data
                daily_increase_list = []
                od_last = False
                date_od_last = False
                od_last_2 = False
                date_od_last_2 = False
                for od in sorted(
                    product.instance_operating_data_ids.filtered("date"),
                    key=lambda d: d.date,
                    reverse=True,
                ):
                    if not od_last:
                        od_last = od.operating_data
                        date_od_last = od.date
                    else:
                        od_last_2 = od.operating_data
                        date_od_last_2 = od.date
                        value_diff = od_last - od_last_2
                        datetime_diff = date_od_last - date_od_last_2
                        days = datetime_diff.days + datetime_diff.seconds / 86400
                        od_last = od_last_2
                        date_od_last = date_od_last_2
                        if days == 0 or value_diff == 0:
                            continue
                        daily_increase = value_diff / days
                        if daily_increase:
                            daily_increase_list.append(daily_increase)
                    i -= 1
                    if i == 0:
                        break
                avg_daily_increase = 1  # default value 1
                if daily_increase_list:
                    avg_daily_increase = sum(daily_increase_list) / len(
                        daily_increase_list
                    )
                for oa in product.operating_appointment_ids:
                    oa.daily_increase = (
                        int(avg_daily_increase) if int(avg_daily_increase) != 0 else 1
                    )
