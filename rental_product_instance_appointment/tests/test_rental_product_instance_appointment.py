# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo.addons.rental_base.tests.stock_common import RentalStockCommon
from odoo import fields


class TestRentalProductInstanceAppointment(RentalStockCommon):
    def setUp(self):
        super().setUp()

        # Product A Created
        ProductObj = self.env["product.product"]
        self.productA = ProductObj.create(
            {
                "name": "Product A",
                "type": "consu",
            }
        )
        self.serialNumberA = self.env["stock.production.lot"].create(
            {
                "name": "Serial Number A",
                "product_id": self.productA.id,
            }
        )
        self.productA.instance_serial_number_id = self.serialNumberA
        self.helpdesk = self.env.ref("rental_repair.project_project_helpdesk")
        self.today = fields.Date.from_string(fields.Date.today())
        self.tomorrow = self.today + relativedelta(days=1)

    def test_00_rental_product_instance_appointment_tasks(self):
        self.productA.write(
            {
                "appointment_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Appointment A",
                            "date_next_appointment": self.today,
                            "leads_of_notification": 1,
                            "time_interval": 1,
                            "time_uom": "month",
                            "product_id": self.productA.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Appointment B",
                            "date_next_appointment": self.today,
                            "leads_of_notification": 1,
                            "time_interval": 10,
                            "time_uom": "day",
                            "product_id": self.productA.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Appointment C",
                            "date_next_appointment": self.tomorrow,
                            "leads_of_notification": 1,
                            "time_interval": 20,
                            "time_uom": "day",
                            "product_id": self.productA.id,
                        },
                    ),
                ],
            }
        )
        self.env["product.appointment"]._cron_gen_update_appointment()
        # Check Appointments
        check_A = check_B = check_C = False
        for appointment in self.productA.appointment_ids:
            if appointment.name == "Appointment A":
                expected_next_appointment = self.today + relativedelta(months=1)
                self.assertEqual(
                    appointment.date_next_appointment, expected_next_appointment
                )
                check_A = True
            if appointment.name == "Appointment B":
                expected_next_appointment = self.today + relativedelta(days=10)
                self.assertEqual(
                    appointment.date_next_appointment, expected_next_appointment
                )
                check_B = True
            if appointment.name == "Appointment C":
                expected_next_appointment = self.today + relativedelta(months=1)
                self.assertEqual(appointment.date_next_appointment, self.tomorrow)
                check_C = True
        self.assertEqual(check_A and check_B and check_C, True)

        # Check Project Tasks
        self.assertEqual(self.productA.task_count, 1)
        self.assertEqual(self.productA.task_ids[0].product_id, self.productA)
        self.assertEqual(self.productA.task_ids[0].name, "Appointment C: Product A")
        self.assertEqual(self.productA.task_ids[0].lot_id, self.serialNumberA)
        self.assertEqual(self.productA.task_ids[0].date_deadline, self.tomorrow)
        self.assertEqual(self.productA.task_ids[0].project_id, self.helpdesk)
