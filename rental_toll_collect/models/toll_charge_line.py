# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from datetime import datetime as dt, timedelta

from odoo import api, fields, models, exceptions, _


class TollChargeLine(models.Model):
    _name = "toll.charge.line"
    _description = "Toll Charge Line"
    _order = "toll_date desc"

    amount = fields.Float(
        string="Toll Charge Amount",
        currency_field="company_currency_id",
    )

    analytic_account = fields.Char(
        string="Analytic Account",
        help="This is the analytic account given in CSV file. "
        "It is not linked to Odoo analytic accounts.",
    )

    axle_class = fields.Char(
        string="Axle Class",
    )

    booking_number = fields.Char(
        string="Booking Number",
    )

    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="product_id.company_id.currency_id",
        readonly=True,
        store=True,
    )

    distance = fields.Float(string="Distance (km)")

    invoiced = fields.Boolean(
        string="Invoiced?",
        compute="_compute_invoiced",
    )

    invoice_id = fields.Many2one(
        string="Invoice",
        related="invoice_line_id.invoice_id",
        store=True,
    )

    invoice_line_id = fields.Many2one(
        comodel_name="account.invoice.line",
        string="Invoice Line",
    )

    sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
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
        comodel_name="product.product",
        string="Product",
        compute="_compute_product_id",
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
        string="Date (CSV)",
    )

    start_time = fields.Char(
        string="Time",
    )

    tariff_model = fields.Char(
        string="Tariff Model",
    )

    toll_date = fields.Datetime(
        string="Date",
        compute="_compute_toll_date",
        store=True,
    )

    toll_type = fields.Selection(
        [("toll", "Toll")],
        string="Type",
    )

    chargeable = fields.Boolean(
        string="Chargeable?",
        default=True,
    )

    weight_class = fields.Char(string="Weight Class")

    editable = fields.Boolean(
        string="Editable",
        compute="_compute_editable",
    )

    @api.multi
    @api.depends("invoice_id")
    def _compute_editable(self):
        for cl in self:
            cl.editable = cl.invoice_id.state == "draft" if cl.invoice_id else True

    @api.multi
    @api.depends(
        "invoice_line_id",
        "invoice_line_id.toll_product_line_ids",
        "invoice_line_id.product_id",
        "chargeable",
    )
    def _compute_invoiced(self):
        for cl in self:
            # When automatically invoicing toll charge lines,
            # the invoice line with the 'rental service' is linked as invoice_line_id.
            # But when when manually invoicing toll charge lines,
            # the line with 'toll charge' product is linked as invoice_line_id.
            # The 'toll charge' position does not have toll_product_line_ids!
            if cl.invoice_line_id.product_id == self.env.ref(
                "rental_toll_collect.product_toll"
            ):
                cl.invoiced = cl.chargeable and cl.invoice_line_id
            else:
                cl.invoiced = (
                    cl.chargeable
                    and cl.invoice_line_id
                    and cl.invoice_line_id.toll_product_line_ids
                )

    @api.multi
    @api.depends("license_plate", "toll_date")
    def _compute_name(self):
        for cl in self:
            cl.name = (
                cl.license_plate + " on " + cl.toll_date.strftime("%Y-%m-%d %H:%M")
            )

    @api.multi
    @api.depends("license_plate")
    def _compute_product_id(self):
        products = self.env["product.product"]
        for cl in self:
            if cl.license_plate:
                prod_domain = [("license_plate", "=", cl.license_plate)]
                product = products.search(prod_domain)
                if len(product) > 1:
                    raise exceptions.ValidationError(
                        _("There are %s vehicles with the license plate '%s'.")
                        % (len(product), cl.license_plate)
                    )
                else:
                    cl.product_id = product

    @api.multi
    @api.depends("start_date", "start_time")
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

    @api.multi
    def update_toll_charge_lines(self):
        for line in self:
            sol = self.env["sale.order.line"].search(
                [
                    ("start_date", "<=", line.toll_date.date()),
                    ("end_date", ">=", line.toll_date.date()),
                    "|",
                    ("display_product_id", "=", line.product_id.id),
                    ("product_id", "=", line.product_id.id),
                ]
            )
            line.write(
                {
                    "sale_line_id": sol.id if len(sol) == 1 else False,
                }
            )

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        res.update_toll_charge_lines()
        return res
