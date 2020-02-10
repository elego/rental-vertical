# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_id = fields.Many2one(
        'product.product', 'Product Instance',
        domain="[('product_instance', '=', True)]")
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", related="product_id.tracking")
    lot_id = fields.Many2one('stock.production.lot', 'Serial Number')
    repair_ids = fields.One2many(
        'repair.order', 'project_task_id',
        string="Repair Orders")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.lot_id = self.product_id.instance_serial_number_id
