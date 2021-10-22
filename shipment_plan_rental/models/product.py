# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        rented_product_id = vals.get("rented_product_id", False)
        if rented_product_id:
            rented_product = self.browse(rented_product_id)
            vals["trans_purchase_request"] = rented_product.trans_purchase_request
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if "trans_purchase_request" in vals:
            for p in self:
                p.rental_service_ids.write(
                    {"trans_purchase_request": p.trans_purchase_request}
                )
        return res
