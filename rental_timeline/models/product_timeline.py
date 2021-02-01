# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from odoo.tools.misc import profile

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ProductTimeline(models.Model):
    _name = "product.timeline"
    _description = "Product Timeline"

    res_model = fields.Char(
        require=True,
    )

    res_id = fields.Integer(
        require=True,
    )

    click_res_model = fields.Char(
        require=True,
    )

    click_res_id = fields.Integer(
        require=True,
    )

    date_start = fields.Datetime(
        "Date Start",
        require=True,
    )

    date_start_formated = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    date_end = fields.Datetime(
        "Date End",
        require=True,
    )

    date_end_formated = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    product_id = fields.Many2one(
        "product.product",
        "Product",
        ondelete="cascade",
        required=True,
    )

    product_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    order_name = fields.Char(
        "Order",
        require=True,
    )

    type = fields.Selection(
        string="Type",
        selection=[
            ("rental", "Rental"),
            ("reserved", "Reserved"),
        ],
    )

    type_formated = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    has_clues = fields.Char(
        "Has Clues",
        compute="_compute_fields",
        store=True,
    )

    redline = fields.Boolean(
        "Redline",
    )

    product_tmpl_id = fields.Many2one(
        related="product_id.product_tmpl_id",
        store=True,
    )

    product_categ_id = fields.Many2one(
        related="product_id.categ_id",
        store=True,
    )

    product_categ_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    name = fields.Char(
        "Name",
        compute="_compute_fields",
        store=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        "Partner",
        ondelete="set null",
        compute="_compute_fields",
        store=True,
    )

    partner_shipping_address = fields.Char(
        "Shipping address",
        compute="_compute_fields",
        store=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_fields",
        store=True,
    )

    price_subtotal = fields.Monetary(
        currency_field="currency_id",
        field_digits=True,
        compute="_compute_fields",
        store=True,
    )

    number_of_days = fields.Integer(
        "Total days",
        compute="_compute_fields",
        store=True,
    )

    rental_period = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    amount = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        compute="_compute_fields",
        store=True,
    )

    warehouse_name = fields.Char(
        compute="_compute_fields",
        store=True,
    )

    action_id = fields.Integer(
        compute="_compute_fields",
        store=True,
    )

    menu_id = fields.Integer(
        compute="_compute_fields",
        store=True,
    )

    _sql_constraints = [
        (
            "date_check",
            "CHECK ((date_start <= date_end))",
            "The start date must be anterior to the end date.",
        ),
    ]

    @api.depends('res_id', 'res_model')
    def _compute_fields(self):
        """ This function should be called for example in _reset_timeline
            of the related res_model, since it will only be triggered, if
            res_id or res_model is changed.
        """
        lang = self.env["res.lang"].search([("code", "=", self.env.user.lang)])
        for line in self:
            date_with_time = False
            if line.res_model == "sale.order.line":
                obj = self.env[line.res_model].browse(line.res_id)
                order_obj = obj.order_id
                line.name = _("R: %s") % order_obj.partner_id.name
                line.partner_id = order_obj.partner_id.id
                line.partner_shipping_address = (
                    order_obj.partner_shipping_id._display_address()
                )

                line.warehouse_id = order_obj.warehouse_id.id
                line.currency_id = obj.currency_id.id
                line.price_subtotal = obj.price_subtotal
                line.number_of_days = obj.number_of_days
                line.rental_period = "{product_uom_qty} {product_uom}".format(
                    product_uom_qty=int(obj.product_uom_qty),
                    product_uom=obj.product_uom.name,
                )
                currency = line.currency_id
                line.amount = "{price_subtotal} {currency}".format(
                    price_subtotal=lang.format(
                        "%.2f", line.price_subtotal, grouping=True
                    ),
                    currency=currency.symbol,
                )
                line.has_clues = False

                if obj.product_uom == self.env.ref("uom.product_uom_hour"):
                    date_with_time = True

            line.product_name = line.product_id.display_name
            line.warehouse_name = line.warehouse_id.display_name
            line.product_categ_name = line.product_categ_id.display_name

            try:
                selections = self.fields_get()["type"]["selection"]
                selection = [s for s in selections if s[0] == line.type][0]
                line.type_formated = selection[1]
            except Exception as e:
                _logger.exception(e)
                line.type_formated = str(line.type)

            datetime_format = lang.date_format
            if date_with_time:
                datetime_format += " " + time.date_format
            if isinstance(line.date_start, datetime):
                line.date_start_formated = line.date_start.strftime(datetime_format)
            else:
                line.date_start_formated = str(line.date_start)
            if isinstance(line.date_end, datetime):
                line.date_end_formated = line.date_end.strftime(datetime_format)
            else:
                line.date_end_formated = str(line.date_end)

            line.action_id = self.env.ref("rental_base.action_rental_orders").id
            line.menu_id = self.env.ref("rental_base.menu_rental_root").id

    @api.model
    @profile('/var/lib/odoo/data/timeline.profile')
    def my_search_read(self):
        my_fields = ["display_name","date_start","date_end","product_id","type","type_formated","has_clues","redline","date_start_formated","date_end_formated","partner_id","partner_shipping_address","currency_id","amount","price_subtotal","number_of_days","rental_period","offday_number","warehouse_id","warehouse_name","product_instance_state","product_instance_state_formated","product_instance_next_service_date","product_instance_current_location_id","product_instance_current_location_name","product_instance_serial_number_id","product_instance_serial_number_name","product_manu_name","product_manu_type_name","product_fleet_type_name","product_name","product_categ_id","product_categ_name","action_id","menu_id","res_model","res_id","click_res_model","click_res_id","order_name","repair","appointment"]
        start = fields.Datetime.now()
        res = self.search_read(fields=my_fields, domain=[])
        end = fields.Datetime.now()
        print(start.strftime('%Y-%m-%d %H:%M:%S.%f'))
        print(end.strftime('%Y-%m-%d %H:%M:%S.%f'))
        #return res
