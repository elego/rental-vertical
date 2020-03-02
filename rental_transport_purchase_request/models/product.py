# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    trans_purchase_request = fields.Boolean("Transport Purchase Request", copy=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'trans_purchase_request' in vals:
            for p in self:
                p.rental_service_ids.write({'trans_purchase_request': p.trans_purchase_request})
