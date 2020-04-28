# Part of rental-vertical See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, exceptions, _


class TollChargeLine(models.Model):
    _name = 'toll.charge.line'
    _description = 'Toll Charge Line'

    def _default_analytic_account(self):
        return self.env.ref('rental_toll_collect.account_analytic_account_maut').id


    vehicle_reg_number = fields.Char(string='Vehicle Registration Number')
    start_date = fields.Datetime(string='Start Date')
    booking_number = fields.Char(string='Booking Number')
    toll_type = fields.Selection([('toll', 'Toll')], string='Type')
    drive = fields.Char(string='Drive')
    drive_via = fields.Char(string='Drive via')
    departure = fields.Char(string='Deaprture')
    cost_centre = fields.Many2one('account.analytic.account',
        string='Cost Centre',
        default=lambda self: self._default_analytic_account())
    tariff_model = fields.Char(string='Tariff Model')
    axis_class = fields.Char(string='Axis Class')
    weight_class = fields.Char(string='Weight Class')
    polution_class = fields.Char(string='Poution Class')
    road_operator = fields.Many2one('res.partner', string='Road Operator')
    procedure = fields.Selection(
        [('AV', 'Automatic Procedure'),
         ('MVM', 'Manual Procedure Toll'),
         ('MVI', 'Manual Procedure Internet'),
         ('MVA', 'Manual Procedure App')],
        string='Procedure')
    kilometer = fields.Float(string='KiloMeter')
    toll_charge = fields.Float(string='Toll Charge')
    is_charges = fields.Boolean(string='Is Charged', default=False)
    toll_product_id = fields.Many2one('product.product',
        string='Toll Product')
    toll_contract_id = fields.Many2one('contract.contract',
        string='Toll Contract')
    toll_invoice_id = fields.Many2one('account.invoice',
        string='Toll Invoice')
