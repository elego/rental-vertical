# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from . import models
from . import wizard

from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search(
        [("administrative_charge_product", "=", False)]
    )
    if companies:
        for company in companies:
            company._set_administrative_charge_product()
            customers = env["res.partner"].search([("company_id", "=", company.id)])
            customers.write(
                {
                    "administrative_charge_product": company.administrative_charge_product.id,
                }
            )
