# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    task_ids = fields.One2many('project.task', 'product_instance_id', string='Tasks')
    task_count = fields.Integer('Task Count', compute="_compute_task_count")
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment', string='Maintenance Equipment',
        ondelete='restrict', index=True)
    #TODO add more related fields from maintenance_equipment_id
    serial_no = fields.Char('Serial Nr.', related="maintenance_equipment_id.serial_no", store=True)
    maintenance_count = fields.Integer('Maintenance Count', related="maintenance_equipment_id.maintenance_count")

    @api.multi
    def _compute_task_count(self):
        for p in self:
            p.task_count = len(p.task_ids)

    @api.multi
    @api.constrains('maintenance_equipment_id')
    def _check_unique_maintenance_equipment(self):
        for rec in self:
            if rec.maintenance_equipment_id:
                domain = [
                    ('maintenance_equipment_id', '=', rec.maintenance_equipment_id.id),
                    ('id', '!=', rec.id),
                ]
                res = self.search_count(domain)
                if res:
                    raise exceptions.ValidationError(
                        _('This Maintenance Equipment was already assigned to another product.'))

    @api.model
    def _create_maintenance_equipment(self, vals):
        res = vals
        instance_serial_number_id = vals.get('instance_serial_number_id', False)
        maintenance_equipment = self.env['maintenance.equipment'].create({
            'name': vals.get('name'),
            'product_instance': True,
            'note': vals.get('notes', False),
            'serial_no':
                instance_serial_number_id and
                self.env['stock.production.lot'].browse(instance_serial_number_id).name,
            'maintenance_team_id':
                vals.get('maintenance_team_id', False) or
                self.env.ref('maintenance.equipment_team_maintenance').id})
        if maintenance_equipment:
            res['maintenance_equipment_id'] = maintenance_equipment.id
        return res

    @api.model
    def create(self, vals):
        new_vals = vals
        if vals.get('product_instance', False):
            new_vals = self._create_maintenance_equipment(new_vals)
        return super().create(new_vals)

    @api.multi
    def unlink(self):
        equipments = self.mapped('maintenance_equipment_id')
        res = super(ProductProduct, self).unlink()
        for equipment in equipments:
            equipment.product_instance = False
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'product_instance' in vals:
            # set product_instance with True
            if vals.get('product_instance', False):
                for product in self:
                    new_vals = {'name': product.name}
                    # create a new equipment
                    if not product.maintenance_equipment_id:
                        new_vals = self._create_maintenance_equipment(new_vals)
                        print(new_vals)
                        product.maintenance_equipment_id = new_vals.get('maintenance_equipment_id', False)
                    # activate the old equipment
                    else:
                        product.maintenance_equipment_id.product_instance = True
            # set product_instance with False
            else:
                for product in self:
                    new_vals = vals
                    # deactivate the old equipment
                    if product.maintenance_equipment_id:
                        product.maintenance_equipment_id.product_instance = False
        return res

    @api.onchange('instance_serial_number_id')
    def onchange_instance_serial_number_id(self):
        if self.instance_serial_number_id:
            self.serial_no = self.instance_serial_number_id.name

    #TODO Check if it should be replaced with the action
    # "maintenance.hr_equipment_request_action_from_equipment"
    @api.multi
    def action_view_maintenance(self):
        self.ensure_one()
        res_model = "maintenance.request"
        record_ids = self.env['maintenance.request'].search(
            [('equipment_id', '=', self.maintenance_equipment_id.id)]).ids
        view_id = self.env.ref("maintenance.hr_equipment_request_view_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Maintenance Orders'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': res_model,
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    @api.multi
    def action_view_project_task(self):
        self.ensure_one()
        res_model = "project.task"
        record_ids = self.env[res_model].search([('product_instance_id', '=', self.id)]).ids
        print(record_ids)
        tree_view_id = self.env.ref("project_task_order.view_project_task_tree").id
        form_view_id = self.env.ref("project.view_task_form2").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Maintenance Orders'),
            'target': 'current',
            'view_mode': "tree,form",
            'view_ids': [tree_view_id, form_view_id],
            'res_model': res_model,
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }
