# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    project_task_id = fields.Many2one('project.task', 'Task', ondelete="set null")

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_instance = fields.Boolean('Product Instance')
