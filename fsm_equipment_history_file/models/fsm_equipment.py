# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class FSMEquipment(models.Model):
    _inherit = 'fsm.equipment'

    owned_by_id = fields.Many2one('res.partner', string='Owned By')
    history_file_id = fields.Many2one('fsm.equipment.history.file', string='History File')

    @api.model
    def create(self, vals):
        res = super(FSMEquipment, self).create(vals)
        if vals.get('history_file_id', False):
            res.history_file_id.equipment_id = res.id
        return res

    @api.multi
    def write(self, vals):
        for equipment in self:
            prev_history_file = equipment.history_file_id
            res = super(FSMEquipment, equipment).write(vals)
            if 'history_file_id' in vals:
                if prev_history_file:
                    prev_history_file.equipment_id = False
                if equipment.history_file_id:
                    equipment.history_file_id.equipment_id = equipment.id
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    history_file_relevant = fields.Boolean(
        string='History File relevant', default=False,
        help='This product is part of a history file.')
    history_file_obligatory = fields.Boolean(
        string='History File obligatory', default=False,
        help='You need to create a history file for this product.')
