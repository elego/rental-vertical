from openupgradelib import openupgrade


def delete_insurance_type(cr):
    query = """DELETE FROM ir_ui_view WHERE arch_db ILIKE '%insurance_type%' AND arch_fs ILIKE 'rockbird_%'"""
    openupgrade.logged_query(cr, query)
    query = """DELETE FROM ir_ui_view WHERE inherit_id IN (SELECT id FROM ir_ui_view WHERE arch_db ilike '%insurance_type%')"""
    openupgrade.logged_query(cr, query)
    query = """DELETE FROM ir_ui_view WHERE arch_db ILIKE '%insurance_type%' AND arch_fs ILIKE 'rental_contract_insurance%'"""
    openupgrade.logged_query(cr, query)
    query = """DELETE FROM ir_ui_view WHERE arch_db ILIKE '%insurance_type%' AND arch_fs ILIKE 'rental_product_insurance%'"""
    openupgrade.logged_query(cr, query)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    delete_insurance_type(cr)
