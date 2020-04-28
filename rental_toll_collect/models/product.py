# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.one
    @api.depends('toll_line_ids.toll_charge', 'toll_line_ids.is_charges')
    def _compute_open_road_charges(self):
        for rec in self:
            rec.toll_amount = rec.get_open_road_charges_amount()
            rec.open_toll_charge_count = len(rec.get_open_road_charges())

    @api.multi
    def get_open_road_charges(self):
        self.ensure_one()
        lines = [line for line in self.toll_line_ids.filtered(
            lambda x: x.is_charges == False)]
        return list(set(lines))

    @api.multi
    def get_open_road_charges_amount(self):
        self.ensure_one()
        return sum(line.toll_charge for line in self.toll_line_ids.filtered(
            lambda x: x.is_charges == False))

    toll_line_ids = fields.One2many(
        'toll.charge.line',
        'toll_product_id',
        string='Toll Charge Lines',
    )
    toll_amount = fields.Monetary(string='Total Toll Charge Amount',
        store=True, readonly=True,
        compute='_compute_open_road_charges',
        track_visibility='always')
    open_toll_charge_count = fields.Integer(
        compute='_compute_open_road_charges',
        string="Open Toll Charge",
        type='integer')

    @api.multi
    def action_view_open_toll_charge(self):
        self.ensure_one()
        record_ids = [rec.id for rec in self.get_open_road_charges()]
        print("====record_ids====", record_ids)
        action = self.env.ref('rental_toll_collect.toll_charge_line_action').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

