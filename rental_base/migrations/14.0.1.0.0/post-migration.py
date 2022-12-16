# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    rental_type_id = env.ref("rental_base.rental_sale_type").id
    orders = env["sale.order"].search([("type_id", "=", rental_type_id)])
    orders._compute_default_start_date()
    orders._compute_default_end_date()
