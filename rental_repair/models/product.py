# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    task_ids = fields.One2many(
        comodel_name="project.task",
        inverse_name="product_id",
        string="Tasks",
    )

    task_count = fields.Integer(
        string="Task Count",
        compute="_compute_task_count",
    )

    repair_order_ids = fields.One2many(
        comodel_name="repair.order",
        inverse_name="product_id",
        string="Repair Orders",
    )

    repair_count = fields.Integer(
        compute="_compute_repair_count",
        string="# Repair Orders",
        help="Total number of Repair Orders",
    )

    def _compute_task_count(self):
        for p in self:
            p.task_count = len(p.task_ids)

    def _compute_repair_count(self):
        for p in self:
            p.repair_count = len(p.repair_order_ids)

    def action_view_project_task(self):
        self.ensure_one()
        res_model = "project.task"
        helpdesk = self.env.ref("rental_repair.project_project_helpdesk")
        record_ids = self.task_ids.ids
        tree_view_id = self.env.ref("rental_repair.view_project_task_tree").id
        form_view_id = self.env.ref("project.view_task_form2").id
        kanban_view_id = self.env.ref("project.view_task_kanban").id
        action_context = {
            "default_product_id": self.id,
            "default_project_id": helpdesk.id,
        }
        return {
            "type": "ir.actions.act_window",
            "name": _("Tickets"),
            "target": "current",
            "view_mode": "kanban,tree,form",
            "view_ids": [kanban_view_id, tree_view_id, form_view_id],
            "res_model": res_model,
            "context": action_context,
            "domain": "[('id','in',[" + ",".join(map(str, record_ids)) + "])]",
        }

    def action_view_repair_history(self):
        self.ensure_one()
        repair_lines = self.env["repair.line"].browse([])
        for repair in self.repair_order_ids:
            repair_lines |= repair.operations
        record_ids = repair_lines.ids
        tree_view_id = self.env.ref("rental_repair.view_product_repair_line_tree").id
        form_view_id = self.env.ref("repair.view_repair_order_form").id
        return {
            "type": "ir.actions.act_window",
            "name": _("Components"),
            "target": "current",
            "view_mode": "tree,form",
            "view_ids": [tree_view_id, form_view_id],
            "res_model": "repair.line",
            "domain": "[('id','in',[" + ",".join(map(str, record_ids)) + "])]",
        }
