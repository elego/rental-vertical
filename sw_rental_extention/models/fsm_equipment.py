# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = "fsm.equipment"

    analytic_account_id = fields.Many2one('account.analytic.account',
                                          string='Analytic Account',
                                          company_dependent=True)
    description = fields.Char('Description') # Bezeichnung
    internal_ref = fields.Char('Internal Reference') # Kurzbezeichnung/Interne Referenz
    other_ref = fields.Char('Other Reference') # Weitere Referenzen
    barcode = fields.Char('Barcode') # Stichcode
    qr_code = fields.Char('QR-Code')
    manu_year = fields.Char('Year of Manufacture')
    sol_ids = fields.One2many('sale.order.line', 'equipment_id', string='Sale Order Lines')
    inv_line_ids = fields.One2many('account.invoice.line', 'equipment_id', string='Invoice Lines')
    po_line_ids = fields.One2many('purchase.order.line', 'equipment_id', string='Purchase Order Lines')
    repair_order_ids = fields.One2many('repair.order', 'equipment_id', string='Repair Orders')
    stock_move_ids = fields.One2many('stock.move', 'equipment_id', string='Stock Moves')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        # clear old selected value
        self.lot_id = False
        self.analytic_account_id = False
