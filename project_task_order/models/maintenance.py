# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    project_task_id = fields.Many2one('project.task', 'Task', ondelete="set null")

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_instance = fields.Boolean('Product Instance')
