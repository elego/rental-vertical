# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    src_forward_shipment_plan_id = fields.Many2one(
        'shipment.plan',
        "Source Forward Shipment Plan",
        ondelete="restrict",
        copy=False,
    )
    dest_forward_shipment_plan_id = fields.Many2one(
        'shipment.plan',
        "Dest Forward Shipment Plan",
        ondelete="restrict",
        copy=False,
    )
    forward_shipment_plan_ids = fields.Many2many(
        'shipment.plan',
        "Forward Shipment Plans",
        compute="_compute_forward_shipment_plan_ids"
    )
    forward_shipment_plan_count = fields.Integer(
        compute="_compute_forward_shipment_plan_ids"
    )

    def _compute_forward_shipment_plan_ids(self):
        for record in self:
            forward_shipment_plans = self.search([
                '|',
                ('src_forward_shipment_plan_id', '=', record.id),
                ('dest_forward_shipment_plan_id', '=', record.id)
            ])
            record.forward_shipment_plan_ids = forward_shipment_plans
            record.forward_shipment_plan_count = len(forward_shipment_plans)

    @api.model
    def _prepare_forward_shipment_plan_values(self, src_shipment_plan, dest_shipment_plan):
        res = {
            'name': 'Forward Shipment Plan for [%s - %s]' %(src_shipment_plan.name, dest_shipment_plan.name),
            'plan_type': 'rental',
            'from_address_id': src_shipment_plan.from_address_id.id,
            'to_address_id': dest_shipment_plan.to_address_id.id,
            'note': "%s \n -------- Forwarding -------\n  %s" %(src_shipment_plan.note, dest_shipment_plan.note),
            'initial_etd': src_shipment_plan.initial_etd,
            'initial_eta': src_shipment_plan.initial_eta,
            'src_forward_shipment_plan_id': src_shipment_plan.id,
            'dest_forward_shipment_plan_id': dest_shipment_plan.id,
            'origin': "%s, %s" %(src_shipment_plan.origin, dest_shipment_plan.origin),
        }
        return res

    @api.multi
    def action_view_forward_shipment_plan(self):
        self.ensure_one()
        action = self.env.ref(
            'shipment_plan.action_shipment_plan'
        ).read([])[0]
        action['domain'] = [('id','in', self.forward_shipment_plan_ids.ids)]
        return action
