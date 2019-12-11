# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_instance_id = fields.Many2one(
        'product.product', 'Product Instance',
        domain="[('product_instance', '=', True)]")
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment', 'Maintenance Equipment',
        related="product_instance_id.maintenance_equipment_id")
    lot_id = fields.Many2one(
        'stock.production.lot',
        related="product_instance_id.instance_serial_number_id")
    maintenance_ids = fields.One2many(
        'maintenance.request', 'project_task_id',
        string="Maintenance Orders")
    repair_ids = fields.One2many(
        'repair.order', 'project_task_id',
        string="Repair Orders")
