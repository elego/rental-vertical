# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    equipment_id = fields.Many2one('fsm.equipment', string='Equipment')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        # clear old selected value
        self.equipment_id = False
        return res

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        # set domain on Analytic Account
        # clear old selected value
        self.account_analytic_id = False
        if self.equipment_id:
            domain = { 'account_analytic_id': [ ('id', '=', self.equipment_id.analytic_account_id.id) ] } 
            return { 'domain': domain }

    @api.model_create_multi
    def create(self, vals_list):
        # update vals_list
        for vals in vals_list:
            inv_type = self.env.context.get('inv_type', 'out_invoice')
            if vals.get('product_id') and not vals.get('equipment_id'):
                product = self.env['product.product'].browse(
                    vals.get('product_id'))
                domain = [('product_id', '=', product.id)]
                equipment = self.env['fsm.equipment'].search(domain, limit=1)
                vals['equipment_id'] = equipment.id or False
                if equipment :
                    ana_account = equipment.analytic_account_id
                    vals['account_analytic_id'] = ana_account.id
        return super().create(vals_list)
