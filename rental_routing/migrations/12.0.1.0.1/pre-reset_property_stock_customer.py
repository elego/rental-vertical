# -*- coding: utf-8 -*-

def migrate(cr, version):
    sql = """UPDATE ir_property
               SET value_reference = 'stock.location,9'
             WHERE name = 'property_stock_customer'
               AND value_reference <> 'stock.location,9'
          """
    cr.execute(sql)
