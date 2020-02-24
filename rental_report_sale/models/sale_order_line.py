# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_sale_order_line_multiline_description_sale(self, product):
        result = super(SaleOrderLine, self).get_sale_order_line_multiline_description_sale(product)
        if self.product_id and self.product_id.default_code:
            code = '[' + self.product_id.default_code + '] '
            if code in result:
                result = result.replace(code, '')
        return result
