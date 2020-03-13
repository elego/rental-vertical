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

    @api.onchange('product_id')
    def onchange_insurance_product_id(self):
        self.insurance_type = 'none'
        if self.product_id:
            if self.product_id.rented_product_id:
                rented_product = self.product_id.rented_product_id
                self.insurance_type = rented_product.insurance_type
                self.insurance_percent = rented_product.insurance_percent

    def _create_rental_insurance_line(self):
        self.ensure_one()
        price_unit = 0
        percent = self.product_id.rented_product_id.insurance_percent
        if self.insurance_type == 'product':
            price_unit = self.product_id.rented_product_id.standard_price
            price_unit = price_unit * percent / 100
        elif self.insurance_type == 'rental':
            price_unit = self.price_subtotal * percent / 100
        insurance_product = self.env.ref(
            'rental_product_insurance.product_product_insurance')
        vals = {
            'name': self.name,
            'product_uom_qty': 1,
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'product_id': insurance_product.id,
            'order_id': self.order_id.id,
        }
        insurance_line = self.env['sale.order.line'].create(vals)
        insurance_line.product_id_change()
        insurance_line.write({
            'name': _('Insurance: %s') % self.name,
            'price_unit': price_unit,
        })
        return insurance_line


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def create_insurcance_cost(self):
        for order in self:
            order_line_vals = []
            for line in order.order_line:
                if line.insurance_type != 'none':
                    line._create_rental_insurance_line()

    @api.multi
    def action_confirm(self):
        self.create_insurcance_cost()
        res = super(SaleOrder, self).action_confirm()
        return res
