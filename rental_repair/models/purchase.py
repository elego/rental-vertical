# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_task_id = fields.Many2one(
        "project.task",
        "Ticket",
        ondelete="set null",
    )
