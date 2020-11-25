# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from . import models
from . import wizard

from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    customers = env['res.partner'].search([
        ('customer', '=', True),
    ])
    customers.write({
        'administrative_charge_product': env.ref('rental_toll_collect.product_administrative_charge').id,
    })
