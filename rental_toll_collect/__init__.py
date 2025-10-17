# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from . import models
from . import wizard


def post_init_hook(env):
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
