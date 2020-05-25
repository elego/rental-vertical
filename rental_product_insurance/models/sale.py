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
    insurance_amount = fields.Float(
        'Insurance Amount',
        compute="_compute_insurance_amount"
    )
    insurance_price_unit = fields.Float(
        'Insurance Amount',
        compute="_compute_insurance_amount"
    )
    insurance_origin_line_id = fields.Many2one(
        'sale.order.line',
        copy=False,
    )
    insurance_line_ids = fields.One2many(
        'sale.order.line',
        'insurance_origin_line_id',
    )
    update_insurance_line = fields.Boolean(
        string='Update Insurance Line',
    )

    @api.onchange(
        'product_uom_qty',
        'product_uom',
        'price_unit',
        'insurance_percent',
        'insurance_type',
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

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

    @api.depends(
        'insurance_percent',
        'insurance_type',
        'product_uom_qty',
        'rental_qty',
        'price_unit',
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
                record.insurance_price_unit = \
                    record.rental_qty * record.insurance_amount / record.product_uom_qty

    def _prepare_rental_insurance_line(self):
        self.ensure_one()
        insurance_product = self.env.ref(
            'rental_product_insurance.product_product_insurance')
        vals = {
            'name': self.name,
            'product_uom_qty': self.product_uom_qty / self.rental_qty,
            'product_uom': self.product_uom.id,
            'product_id': insurance_product.id,
            'insurance_origin_line_id': self.id,
            'order_id': self.order_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return vals

    def _create_rental_insurance_line(self):
        self.ensure_one()
        vals = self._prepare_rental_insurance_line()
        insurance_line = self.env['sale.order.line'].create(vals)
        insurance_line.product_id_change()
        insurance_line.write({
            'name': _('Insurance: %s') % self.name,
            'product_uom': self.product_uom.id,
            'price_unit': self.insurance_price_unit,
        })
        self.update_insurance_line = False
        return insurance_line

    @api.multi
    def update_rental_insurance_line(self):
        self.ensure_one()
        if not self.insurance_line_ids:
            return self._create_rental_insurance_line()
        self.insurance_line_ids.write({
            'product_uom_qty': self.product_uom_qty / self.rental_qty,
            'product_uom': self.product_uom.id,
            'price_unit': self.insurance_price_unit,
        })
        self.update_insurance_line = False
        return self.insurance_line_ids

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res['account_analytic_id'] = rental_product.income_analytic_account_id.id
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.insurance_type != 'none':
            res._create_rental_insurance_line()
        return res
