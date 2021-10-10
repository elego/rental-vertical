# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_rental_contract = fields.Boolean(
        string="Rental Contracts",
        help="If activated, rental contracts are automatically created "
        "from monthly rentals for periodic invoicing.",
    )
    module_rental_product_instance = fields.Boolean(
        string="Product Instance",
        help="If activated, product variants can be used as unique " "instances.",
    )
    module_rental_product_instance_appointment = fields.Boolean(
        string="Appointments for Product Instances",
        help="If activated, project tasks are automatically created "
        "for appointments of product instances.",
    )
    module_rental_product_pack = fields.Boolean(
        string="Rental Product Packs",
        help="If activated, rental orders for product packs will "
        "also update the stock of pack components.",
    )
    module_rental_product_set = fields.Boolean(
        string="Rental Product Sets",
        help="If activated, rental products can be grouped in a set "
        "for usage in rental orders.",
    )
    module_rental_product_variant = fields.Boolean(
        string="Product Variant",
        help="If activated, product variants are used with several "
        "new attributes and smartbuttons.",
    )
    module_rental_repair = fields.Boolean(
        string="Repair Orders for Product Instances",
        help="If activated, repair orders can be managed for product "
        "instances, including the creation of account analytic lines"
        "for the repair costs.",
    )
    module_rental_offday = fields.Boolean(
        string="Rental Off-Days",
        help="If activated, off-days can be calculated for daily "
        "rentals which are excluded from price calculation.",
    )
    module_rental_pricelist = fields.Boolean(
        string="Rental Prices",
        help="If activated, rental prices can be configured for "
        "hourly, daily or monthly rentals.",
    )
    module_rental_timeline = fields.Boolean(
        string="Timeline",
        help="If activated, a timeline for all rental orders (and "
        "others, e.g. repair orders) is shown as overview.",
    )
