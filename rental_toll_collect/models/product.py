# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    toll_line_ids = fields.One2many(
        comodel_name='toll.charge.line',
        inverse_name='product_id',
        string="Toll Charge Lines",
        help="These are all toll charge lines related to this product.",
    )

    toll_amount = fields.Monetary(
        string="Open Toll Charges",
        help="This is the total amount of not yet invoiced toll charges for this product.",
        compute='_compute_open_toll_charges',
        store=True,
        readonly=True,
        track_visibility='always',
    )

    open_toll_charge_count = fields.Integer(
        string="# Open Toll Charge Lines",
        help="This is the number of not yet invoiced toll charge lines related to this product.",
        compute='_compute_open_toll_charges',
        type='integer')

    @api.one
    @api.depends('toll_line_ids.amount', 'toll_line_ids.invoiced', 'toll_line_ids.chargeable')
    def _compute_open_toll_charges(self):
        for rec in self:
            rec.toll_amount = rec.get_open_toll_charges_amount()
            rec.open_toll_charge_count = len(rec.get_open_toll_charges())

    @api.multi
    def get_open_toll_charges(self):
        self.ensure_one()
        lines = [line for line in self.toll_line_ids.filtered(
            lambda x: x.invoiced is False and x.chargeable is True)]
        return list(set(lines))

    @api.multi
    def get_open_toll_charges_amount(self):
        self.ensure_one()
        return sum(line.amount for line in self.toll_line_ids.filtered(
            lambda x: x.invoiced is False and x.chargeable is True))

    @api.multi
    def action_view_open_toll_charge(self):
        self.ensure_one()
        record_ids = [rec.id for rec in self.get_open_toll_charges()]
        # print("====record_ids====", record_ids)
        action = self.env.ref('rental_toll_collect.toll_charge_line_action').read([])[0]
        action['domain'] = [('id', 'in', record_ids)]
        return action

