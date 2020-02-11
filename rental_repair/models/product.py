# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    task_ids = fields.One2many('project.task', 'product_id', string='Tasks')
    task_count = fields.Integer('Task Count', compute="_compute_task_count")
    repair_order_ids = fields.One2many('repair.order', 'product_id', string='Repair Orders')

    @api.multi
    def _compute_task_count(self):
        for p in self:
            p.task_count = len(p.task_ids)

    @api.multi
    def action_view_project_task(self):
        self.ensure_one()
        res_model = "project.task"
        record_ids = self.env[res_model].search([('product_id', '=', self.id)]).ids
        tree_view_id = self.env.ref("rental_repair.view_project_task_tree").id
        form_view_id = self.env.ref("project.view_task_form2").id
        action_context = {
            'default_product_id': self.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Maintenance Orders'),
            'target': 'current',
            'view_mode': "tree,form",
            'view_ids': [tree_view_id, form_view_id],
            'res_model': res_model,
            'context': action_context,
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    @api.multi
    def action_view_repair_history(self):
        self.ensure_one()
        repair_lines = self.env['repair.line'].browse([])
        for repair in self.repair_order_ids:
            repair_lines |= repair.operations
        record_ids = repair_lines.ids
        tree_view_id = self.env.ref("rental_repair.view_product_repair_line_tree").id
        form_view_id = self.env.ref("repair.view_repair_order_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Components'),
            'target': 'current',
            'view_mode': "tree,form",
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'repair.line',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }


