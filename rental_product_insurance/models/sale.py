# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insurance_type = fields.Selection(
        string='Insurance Type',
        selection=[
            ('none', 'None'),
            ('product', 'Cost of Product'),
            ('rental', 'Cost of Rental'),
        ],
        default="none",
    )
    insurance_percent = fields.Float(
        'Insurance Percent'
    )
    insurance_price_unit = fields.Float(
        'Insurance Amount',
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
    insurance_product_ids = fields.Many2many(
        'product.product',
        'insurance_product_sol_rel',
        'sol_id',
        'product_id',
        string='Insurance Products',
        domain=lambda self: [
            ('is_insurance', '=', True),
        ],
    )

    @api.constrains('insurance_product_ids', 'product_uom')
    def _check_insurance_product_uom(self):
        for rec in self:
            res = rec.insurance_product_ids.filtered(
                lambda product: product.uom_id != rec.product_uom)
        if res:
            raise exceptions.ValidationError(
                _('Uom of the selected Insurance product should be same as the sale order line'))

    @api.onchange(
        'product_uom_qty',
        'product_uom',
        'price_unit',
        'insurance_percent',
        'insurance_type',
        'insurance_product_ids',
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

    @api.onchange('product_id', 'product_uom')
    def onchange_insurance_product_id(self):
        self.insurance_type = 'none'
        insurance_product = self.env.ref(
            'rental_product_insurance.product_product_insurance')
        if self.product_id:
            if self.product_id.rented_product_id:
                rented_product = self.product_id.rented_product_id
                self.insurance_type = rented_product.insurance_type
                self.insurance_percent = rented_product.insurance_percent
                self.insurance_product_ids = insurance_product
            else:
                self.insurance_type = self.product_id.insurance_type
                self.insurance_percent = self.product_id.insurance_percent
                self.insurance_product_ids = insurance_product

    @api.onchange(
        'insurance_percent',
        'insurance_type',
        'product_uom_qty',
        'rental_qty',
        'price_unit',
    )
    def onchange_insurance_amount(self):
        insurance_amount = 0
        self.insurance_price_unit = 0
        percent = self.insurance_percent
        if self.insurance_type == 'product':
            price = self.product_id.rented_product_id.standard_price
            insurance_amount = price * percent / 100
        elif self.insurance_type == 'rental':
            insurance_amount = self.price_subtotal * percent / 100
        if self.rental and self.product_uom_qty:
            self.insurance_price_unit = \
                self.rental_qty * insurance_amount / self.product_uom_qty

    @api.onchange(
        'product_uom_qty',
        'product_uom',
        'price_unit',
        'insurance_percent',
        'insurance_type',
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

    def _prepare_rental_insurance_line(self, product):
        self.ensure_one()
        vals = {
            'name': product.name,
            'product_uom_qty': self.product_uom_qty / self.rental_qty,
            'product_uom': self.product_uom.id,
            'product_id': product.id,
            'insurance_origin_line_id': self.id,
            'order_id': self.order_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return vals

    def _create_rental_insurance_line(self, product):
        self.ensure_one()
        vals = self._prepare_rental_insurance_line(product)
        insurance_line = self.env['sale.order.line'].create(vals)
        insurance_line.product_id_change()
        insurance_line.write({
            'name': product.name,
            'price_unit': self.insurance_price_unit,
        })
        return insurance_line

    @api.multi
    def update_rental_insurance_line(self):
        self.ensure_one()
        old_insurance_lines = self.insurance_line_ids
        for product in self.insurance_product_ids:
            insurance_line = False
            for line in old_insurance_lines:
                if line.product_id == product:
                    insurance_line = line
                    old_insurance_lines -= insurance_line
            if not insurance_line:
                insurance_line = self._create_rental_insurance_line(product)
            insurance_line.write({
                'product_uom_qty': self.product_uom_qty / self.rental_qty,
                'product_uom': self.product_uom.id,
                'price_unit': self.insurance_price_unit,
            })
        if old_insurance_lines:
            old_insurance_lines.unlink()
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
            for product in res.insurance_product_ids:
                res._create_rental_insurance_line(product)
            res.update_insurance_line = False
        return res
