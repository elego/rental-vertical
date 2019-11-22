# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

# from odoo import api, fields, models, _


# class StockMoveLine(models.Model):
#     _inherit = "fsm.equipment"

#     analytic_account_id = fields.Many2one('account.analytic.account',
#     	                                  string='Analytic Account',
#                                           company_dependent=True)

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     res = super()._onchange_product_id()
    #     self.equipment_id = False
    #     return res