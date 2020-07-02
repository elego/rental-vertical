# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    date_start = fields.Date(related="start_date", store=True)
    date_end = fields.Date(related="end_date", store=True)

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
        customer_contract = self.env.ref('rental_contract.customer_contract_type')
        customer_rental_contract = self.env.ref('rental_contract.customer_rental_contract_type')

        if res:
            if self.type_id.id == so_normal_order.id:
                type_id = customer_contract
            if self.type_id.id == so_rental_order.id:
                type_id = customer_rental_contract
            res.update({
                'type_id': type_id.id,
                'sale_type_id': self.type_id.id
            })
        return res

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.type_id:
            res['sale_type_id'] = self.type_id.id
        return res
