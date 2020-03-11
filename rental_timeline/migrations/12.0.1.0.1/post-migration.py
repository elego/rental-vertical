from openupgradelib import openupgrade


def fix_order_names(env):
    for pt in env['product.timeline'].search([]):
        obj = env[pt.click_res_model].browse(pt.click_res_id)
        pt.order_name = obj.name

@openupgrade.migrate()
def migrate(env, version):
    fix_order_names(env)
