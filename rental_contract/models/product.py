# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('is_contract', 'rental_ok')
    def onchange_is_contract_rental_ok(self):
        template = self.env.ref('rental_contract.rental_contract_template')
        if self.is_contract and self.rental_ok:
            self.contract_template_id = template.id

    @api.multi
    def _get_contract_ids(self, contract_type="sale"):
        self.ensure_one()
        cls = self.env['contract.line'].search([
            ('product_id','=',self.id)])
        return list(set([l.contract_id.id for l in cls if l.contract_id.contract_type == contract_type]))

    @api.multi
    def action_view_supplier_contract(self):
        self.ensure_one()
        record_ids = self._get_contract_ids(contract_type='purchase')
        for rental_service in self.rental_service_ids: 
            record_ids += rental_service._get_contract_ids(contract_type='purchase')
        record_ids = list(set(record_ids))
        action = self.env.ref('contract.action_supplier_contract').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_customer_contract(self):
        self.ensure_one()
        record_ids = self._get_contract_ids()
        for rental_service in self.rental_service_ids: 
            record_ids += rental_service._get_contract_ids()
        record_ids = list(set(record_ids))
        action = self.env.ref('contract.action_customer_contract').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action
