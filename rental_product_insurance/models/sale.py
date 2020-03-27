# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('none', 'None'),
            ('product', 'Cost of Product'),
            ('rental', 'Cost of rental'),
        ],
        default="none",
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )
    insurance_origin_line_id = fields.Many2one(
        'sale.order.line',
    )

    @api.onchange('product_id')
    def onchange_insurance_product_id(self):
        self.insurance_type = 'none'
        if self.product_id:
            if self.product_id.rented_product_id:
                rented_product = self.product_id.rented_product_id
                self.insurance_type = rented_product.insurance_type
                self.insurance_percent = rented_product.insurance_percent
            else:
                self.insurance_type = self.product_id.insurance_type
                self.insurance_percent = self.product_id.insurance_percent

    def _prepare_rental_insurance_line(self):
        self.ensure_one()
        insurance_product = self.env.ref(
            'rental_product_insurance.product_product_insurance')
        vals = {
            'name': self.name,
            'product_uom_qty': 1,
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'product_id': insurance_product.id,
            'insurance_origin_line_id': self.id,
            'order_id': self.order_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
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
        insurance_line.write({
            'name': _('Insurance: %s') % self.name,
            'price_unit': price_unit,
        })
        return insurance_line

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res['analytic_account_id'] = rental_product.income_analytic_account_id.id
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.insurance_type != 'none':
            res._create_rental_insurance_line()
        return res
