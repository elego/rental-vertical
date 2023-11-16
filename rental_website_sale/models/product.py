# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)
        product_id = self.env['product.product'].browse(combination_info['product_id'])
        instance_condition_hour = product_id.instance_condition_hour
        instance_serial_number_id = product_id.instance_serial_number_id.name
        product_identification_number = product_id.product_identification_number
        vehicle_number = product_id.vehicle_number
        init_regist = product_id.init_regist
        manu_year = product_id.manu_year
        contact_name = product_id.contact_name
        contact_email = product_id.contact_email
        contact_phone = product_id.contact_phone

        combination_info.update(
            instance_condition_hour = instance_condition_hour,
            instance_serial_number_id = instance_serial_number_id,
            product_identification_number = product_identification_number,
            vehicle_number = vehicle_number,
            init_regist = init_regist,
            manu_year = manu_year,
            contact_name = contact_name,
            contact_email = contact_email,
            contact_phone = contact_phone,
        )

        return combination_info