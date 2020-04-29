# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from datetime import datetime as dt, timedelta

from odoo import api, fields, models, exceptions, _


class TollChargeLine(models.Model):
    _name = 'toll.charge.line'
    _description = 'Toll Charge Line'

    def _default_analytic_account(self):
        return self.env.ref('rental_toll_collect.account_analytic_account_maut').id


    vehicle_reg_number = fields.Char(string='Vehicle Registration Number')
    start_date = fields.Datetime(string='Date')
    start_time = fields.Char(string='Start')
    start_dt = fields.Datetime(string='Start Datetime', compute='_compute_start_dt')
    booking_number = fields.Char(string='Booking Number')
    toll_type = fields.Selection([('toll', 'Toll')], string='Type')
    drive = fields.Char(string='Drive')
    drive_via = fields.Char(string='Drive via')
    departure = fields.Char(string='Departure')
    cost_center= fields.Char(string='Cost Center')
    # cost_center = fields.Many2one('account.analytic.account',
    #     string='Cost Center',
    #     default=lambda self: self._default_analytic_account())
    tariff_model = fields.Char(string='Tariff Model')
    axis_class = fields.Char(string='Axis Class')
    weight_class = fields.Char(string='Weight Class')
    polution_class = fields.Char(string='Pollution Class')
    road_operator = fields.Char(string='Road Operator')
    # road_operator = fields.Many2one('res.partner', string='Road Operator')
    procedure = fields.Selection(
        [('AV', 'Automatic Procedure'),
         ('MVM', 'Manual Procedure Toll'),
         ('MVI', 'Manual Procedure Internet'),
         ('MVA', 'Manual Procedure App')],
        string='Procedure')
    kilometer = fields.Float(string='Kilometer')
    toll_charge = fields.Float(string='Toll Charge')
    is_charges = fields.Boolean(string='Is Charged', default=False)
    toll_product_id = fields.Many2one('product.product',
        string='Toll Product')
    toll_contract_id = fields.Many2one('contract.contract',
        string='Toll Contract')
    toll_invoice_id = fields.Many2one('account.invoice',
        string='Toll Invoice')

    @api.multi
    @api.depends('start_date', 'start_time')
    def _compute_start_dt(self):
        for cl in self:
            if cl.start_date:
                if cl.start_time:
                    start = dt.strptime(cl.start_time, "%H:%M")
                    offset = start - dt.strptime("00:00", "%H:%M")
                    cl.start_dt = cl.start_date + offset
                else:
                    cl.start_dt = cl.start_date
            else:
                cl.start_dt = False
