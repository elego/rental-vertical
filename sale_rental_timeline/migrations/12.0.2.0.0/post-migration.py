from openupgradelib import openupgrade


def fix_models_and_ids(cr):
    openupgrade.logged_query(
        cr, """
            UPDATE product_timeline
            SET
                res_model = 'sale.order.line',
                order_res_id = sol.order_id,
                order_res_model = 'sale.order'
            FROM sale_order_line sol
            WHERE
                res_id = sol.id;
        """
    )

@openupgrade.migrate()
def migrate(env, version):
    fix_models_and_ids(env.cr)
