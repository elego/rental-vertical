# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    rental_price_interval_rule_ids = fields.One2many(
        "rental.price.interval.rule",
        "company_id",
        string="Rental Interval Price Rules",
    )


class RentalPriceIntervalRule(models.Model):
    _name = "rental.price.interval.rule"
    _description = "Rental Price Interval Rule"

    name = fields.Char(
        "Name",
    )

    factor = fields.Float(
        "Factor",
    )

    min_quantity = fields.Integer(
        "Interval (days)",
    )

    company_id = fields.Many2one(
        "res.company",
        "Company",
    )
