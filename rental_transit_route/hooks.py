# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    env.ref('stock.warehouse0').write({'rental_allowed': False})
    env.ref('stock.warehouse0').write({'rental_allowed': True})
