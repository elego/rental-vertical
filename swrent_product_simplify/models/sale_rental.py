# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)


class SaleRental(models.Model):
    _inherit = 'sale.rental'

    @api.depends(
        'start_order_line_id', 'extension_order_line_ids.end_date',
        'extension_order_line_ids.state', 'start_order_line_id.end_date')
    def name_get(self):
        res = super().name_get()
        for rental in self:
            name = '[%s] %s - %s > %s (%s)' % (
                rental.partner_id.name,
                rental.rental_product_id.name,
                rental.start_date,
                rental.end_date,
                rental._fields['state'].convert_to_export(rental.state, rental)
            )
            res.append((rental.id, name))
        return res