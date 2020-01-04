# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rental_uom_id = fields.Many2one('uom.uom', string='Rental Unit of Measure')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('rented_product_id', 'must_have_dates', 'type', 'uom_id')
    def _check_rental(self):
        day_uom = self.env.ref('uom.product_uom_day')
        for product in self:
            if product:
                if not product.must_have_dates:
                    raise ValidationError(_(
                        "The rental product '%s' must have the option "
                        "'Must Have Start and End Dates' checked.")
                        % product.name)
                # In the future, we would like to support all time UoMs
                # but it is more complex and requires additionnal developments
                if product.rental_uom_id != day_uom:
                    raise ValidationError(_(
                        "The unit of measure of the rental product '%s' must "
                        "be 'Day'.") % product.name)
            # if product.rented_product_id:
                # if product.type != 'service':
                #     raise ValidationError(_(
                #         "The rental product '%s' must be of type 'Service'.")
                #         % product.name)