# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_rental_insurance_line(self):
        self.ensure_one()
        vals = super()._prepare_rental_insurance_line()
        contract_insurance_product = self.env.ref(
            'rental_contract_insurance.product_product_contract_insurance')
        uom_month = self.env.ref('rental_base.product_uom_month')
        if self.product_uom == uom_month:
            vals['product_id'] = contract_insurance_product.id
            vals['date_start'] = self.start_date
            vals['date_end'] = self.end_date
            vals['start_date'] = self.start_date
            vals['end_date'] = self.end_date
        return vals
        
    def _create_rental_insurance_line(self):
        self.ensure_one()
        price_unit = 0
        percent = self.product_id.rented_product_id.insurance_percent
        if self.insurance_type == 'product':
            price_unit = self.product_id.rented_product_id.standard_price
            price_unit = price_unit * percent / 100
        elif self.insurance_type == 'rental':
            price_unit = self.price_subtotal * percent / 100
        vals = self._prepare_rental_insurance_line()
        insurance_line = self.env['sale.order.line'].create(vals)
        insurance_line.product_id_change()
        insurance_line.onchange_product()
        insurance_line.write({
            'name': _('Insurance: %s') % self.name,
            'price_unit': price_unit,
            'date_start': vals['date_start'],
            'date_end' : vals['date_end'],
            'start_date': vals['start_date'],
            'end_date' : vals['end_date'],
        })
        return insurance_line

    @api.multi
    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        res = super(SaleOrderLine, self)._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res['analytic_account_id'] = rental_product.income_analytic_account_id.id
        return res

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res['analytic_account_id'] = rental_product.income_analytic_account_id.id
        return res
