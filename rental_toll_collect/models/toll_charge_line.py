# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from datetime import datetime as dt, timedelta

from odoo import api, fields, models, exceptions, _


class TollChargeLine(models.Model):
    _name = 'toll.charge.line'
    _description = 'Toll Charge Line'
    _order = 'toll_date desc'

    amount = fields.Float(
        string='Toll Charge Amount',
        currency_field='company_currency_id',
    )

    analytic_account = fields.Char(
        string="Analytic Account",
        help="This is the analytic account given in CSV file. "
             "It is not linked to Odoo analytic accounts."
    )

    axle_class = fields.Char(
        string="Axle Class",
    )

    booking_number = fields.Char(
        string="Booking Number",
    )

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='product_id.company_id.currency_id',
        readonly=True, store=True)

    distance = fields.Float(
        string="Distance (km)"
    )

    invoiced = fields.Boolean(
        string='Invoiced?',
        compute="_compute_invoiced",
    )

    invoice_id = fields.Many2one(
        string="Invoice",
        related="invoice_line_id.invoice_id",
        store=True,
    )

    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line',
        string="Invoice Line",
    )

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Sale Order Line",
    )

    license_plate = fields.Char(
        string="License Plate",
    )

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
    )

    polution_class = fields.Char(
        string="Pollution Class",
    )

    procedure = fields.Selection(
        [
            ("AV", "Automatic Procedure"),
            ("MVM", "Manual Procedure Toll"),
            ("MVI", "Manual Procedure Internet"),
            ("MVA", "Manual Procedure App"),
        ],
        string="Procedure",
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        compute='_compute_product_id',
        store=True,
    )

    road_operator = fields.Char(
        string="Road Operator",
    )

    route_exit = fields.Char(
        string="Exit",
    )

    route_ramp = fields.Char(
        string="Ramp",
    )

    route_via = fields.Char(
        string="Drive via",
    )

    start_date = fields.Datetime(
        string="Date",
    )

    start_time = fields.Char(
        string="Time",
    )

    tariff_model = fields.Char(
        string="Tariff Model",
    )

    toll_date = fields.Datetime(
        string="Date",
        compute='_compute_toll_date',
        store=True,
    )

    toll_type = fields.Selection(
        [
            ("toll", "Toll")
        ],
        string="Type",
    )

    chargeable = fields.Boolean(
        string='Chargeable?',
        default=True,
    )

    weight_class = fields.Char(
        string='Weight Class'
    )

    @api.multi
    @api.depends('invoice_line_id', 'invoice_line_id.toll_product_line_ids', 'chargeable')
    def _compute_invoiced(self):
        for cl in self:
            cl.invoiced = cl.chargeable and cl.invoice_line_id and cl.invoice_line_id.toll_product_line_ids

    @api.multi
    @api.depends('license_plate', 'toll_date')
    def _compute_name(self):
        for cl in self:
            cl.name = cl.license_plate + " on " + cl.toll_date.strftime("%Y-%m-%d %H:%M")

    @api.multi
    @api.depends('license_plate')
    def _compute_product_id(self):
        products = self.env['product.product']
        for cl in self:
            if cl.license_plate:
                prod_domain = [('license_plate', '=', cl.license_plate)]
                product = products.search(prod_domain)
                if len(product) > 1:
                    raise exceptions.ValidationError(
                        _("There are %s vehicles with the license plate '%s'.")
                        % (len(product), cl.license_plate)
                    )
                else:
                    cl.product_id = product

    @api.multi
    @api.depends('start_date', 'start_time')
    def _compute_toll_date(self):
        for cl in self:
            if cl.start_date:
                if cl.start_time:
                    start = dt.strptime(cl.start_time, "%H:%M")
                    offset = start - dt.strptime("00:00", "%H:%M")
                    cl.toll_date = cl.start_date + offset
                else:
                    cl.toll_date = cl.start_date
            else:
                cl.toll_date = False
