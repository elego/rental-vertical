# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insurance_entire_time = fields.Boolean(
        'Insurance for entire Time',
        default=True,
    )

    @api.depends(
        'insurance_percent',
        'insurance_type',
        'product_uom_qty',
        'rental_qty',
        'price_unit',
        'insurance_entire_time',
    )
    def _compute_insurance_amount(self):
        for record in self:
            record.insurance_amount = 0
            record.insurance_price_unit = 0
            percent = record.insurance_percent
            if record.insurance_type == 'product':
                price = record.product_id.rented_product_id.standard_price
                record.insurance_amount = price * percent / 100
            elif record.insurance_type == 'rental':
                record.insurance_amount = record.price_subtotal * percent / 100
            if record.rental and record.product_uom_qty:
                if record.insurance_entire_time and record.number_of_time_unit:
                    record.insurance_price_unit = record.insurance_amount / record.number_of_time_unit
                else:
                    record.insurance_price_unit = \
                        record.rental_qty * record.insurance_amount / record.product_uom_qty

    @api.onchange(
        'product_uom_qty',
        'product_uom',
        'price_unit',
        'insurance_percent',
        'insurance_type',
        'insurance_entire_time',
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

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
        return vals
        
    def _create_rental_insurance_line(self):
        self.ensure_one()
        uom_month = self.env.ref('rental_base.product_uom_month')
        vals = self._prepare_rental_insurance_line()
        insurance_line = self.env['sale.order.line'].create(vals)
        insurance_line.product_id_change()
        insurance_line.write({
            'name': _('Insurance: %s') % self.name,
            'product_uom': self.product_uom.id,
            'price_unit': self.insurance_price_unit,
        })
        self.update_insurance_line = False
        if self.product_uom == uom_month:
            insurance_line.onchange_product()
            insurance_line.write({
                'date_start': vals['date_start'],
                'date_end' : vals['date_end'],
            })
        return insurance_line

    @api.multi
    def update_rental_insurance_line(self):
        self.ensure_one()
        if not self.insurance_line_ids:
            return self._create_rental_insurance_line()
        qty = self.product_uom_qty / self.rental_qty
        if self.insurance_entire_time:
            qty = self.number_of_time_unit
        self.insurance_line_ids.write({
            'product_uom_qty': qty,
            'product_uom': self.product_uom.id,
            'price_unit': self.insurance_price_unit,
        })
        self.update_insurance_line = False
        return self.insurance_line_ids

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
                res['account_analytic_id'] = rental_product.income_analytic_account_id.id
        return res
