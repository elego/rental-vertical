# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    project_task_id = fields.Many2one('project.task', 'Task', ondelete="set null")

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(RepairOrder, self).onchange_product_id()
        if self.product_id and self.product_id.instance_serial_number_id:
            self.lot_id = self.product_id.instance_serial_number_id.id
