# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('end_date')
    def end_date_change(self):
        res = super(SaleOrderLine, self).end_date_change()
        if self.end_date:
            self.date_end = self.end_date

    @api.onchange('start_date')
    def start_date_change(self):
        res = super(SaleOrderLine, self).start_date_change()
        if self.start_date:
            self.date_start = self.start_date

    @api.multi
    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        res = super(SaleOrderLine, self)._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id)
        if self.product_id.income_analytic_account_id:
            res['analytic_account_id'] = self.product_id.income_analytic_account_id.id
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _prepare_contract_value(self, contract_template):
        res = super(SaleOrder, self)._prepare_contract_value(contract_template)
        so_normal_order = self.env.ref('sale_order_type.normal_sale_type')
        so_rental_order = self.env.ref('rental_base.rental_sale_type')
        cn_normal_order = self.env.ref('rental_contract.normal_contract_type')
        cn_rental_order = self.env.ref('rental_contract.rental_contract_type')

        if res:
            if self.type_id.id == so_normal_order.id:
                type_id = cn_normal_order.id
            if self.type_id.id == so_rental_order.id:
                type_id = cn_rental_order.id
            res.update({
                'type_id': type_id,
                'sale_type_id': self.type_id.id
            })
            res['code'] = self.name
        return res
