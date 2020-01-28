# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sale_rental_pricelist = fields.Boolean("Price Extension", help="Set Rental Price with different Unit of Measure.")
    module_sale_rental_timeline = fields.Boolean("Timelines")
    module_rental_product_pack = fields.Boolean("Product Pack")
    module_rental_product_variant = fields.Boolean("Product Variant")
    module_rental_product_instance = fields.Boolean("Product Instance")
    module_rental_product_set = fields.Boolean("Product Set")
    module_rental_contract = fields.Boolean("Contract")
    module_rental_repair = fields.Boolean("Repair Order")


    #def set_values(self):
    #super(ResConfigSettings, self).set_values()

    #@api.model
    #def get_values(self):
    #    res = super(ResConfigSettings, self).get_values()
    #    return res
