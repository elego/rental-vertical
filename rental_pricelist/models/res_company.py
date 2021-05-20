# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    rental_service_name_prefix_day = fields.Char(
        "Prefix of Rental Service Name (Day)",
        default="Rental of",
    )
    rental_service_name_prefix_month = fields.Char(
        "Prefix of Rental Service Name (Month)",
        default="Rental of",
    )
    rental_service_name_prefix_hour = fields.Char(
        "Prefix of Rental Service Name (Hour)",
        default="Rental of",
    )
    rental_service_name_suffix_day = fields.Char(
        "Suffix of Rental Service Name (Day)",
        default="(Day(s))",
    )
    rental_service_name_suffix_month = fields.Char(
        "Suffix of Rental Service Name (Month)",
        default="(Month(s))",
    )
    rental_service_name_suffix_hour = fields.Char(
        "Suffix of Rental Service Name (Hour)",
        default="(Hour(s))",
    )
    rental_service_default_code_prefix_day = fields.Char(
        "Prefix of Rental Service Internal Reference (Day)",
        default="RENT-D",
    )
    rental_service_default_code_prefix_month = fields.Char(
        "Prefix of Rental Service Internal Reference (Month)",
        default="RENT-M",
    )
    rental_service_default_code_prefix_hour = fields.Char(
        "Prefix of Rental Service Internal Reference (Hour)",
        default="RENT-H",
    )
    rental_service_default_code_suffix_day = fields.Char(
        "Suffix of Rental Service Internal Reference (Day)",
    )
    rental_service_default_code_suffix_month = fields.Char(
        "Suffix of Rental Service Internal Reference (Month)",
    )
    rental_service_default_code_suffix_hour = fields.Char(
        "Suffix of Rental Service Internal Reference (Hour)",
    )
