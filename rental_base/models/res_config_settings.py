# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sale_rental_pricelist = fields.Boolean("Price Extension", help="Set Rental Price with different Unit of Measure.")
    module_sale_rental_timeline = fields.Boolean("Timelines")
    module_rental_product_pack = fields.Boolean("Product Pack")
    module_rental_product_variant = fields.Boolean("Product Variant")
    module_rental_product_instance = fields.Boolean("Product Instance")


    #def set_values(self):
    #super(ResConfigSettings, self).set_values()

    #@api.model
    #def get_values(self):
    #    res = super(ResConfigSettings, self).get_values()
    #    return res
