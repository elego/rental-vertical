from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


def set_property_stock_customer(env):
    customers = env["res.partner"].search(
        [
            ("customer", "=", True),
        ]
    )
    companies = env["res.company"].search([])
    for company in companies:
        customers.with_context(force_company=company.id).write(
            {"property_stock_customer": env.ref("stock.stock_location_customers").id}
        )
        _logger.info(
            "update property_stock_customer for customer (IDs: %s) (Company: %s)"
            % (customers.ids, company.id)
        )


@openupgrade.migrate()
def migrate(env, version):
    set_property_stock_customer(env)
