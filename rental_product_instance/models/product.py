# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression


class ProductCategory(models.Model):
    _inherit = "product.category"

    show_instance_condition_type = fields.Selection(
        string="Show Instance Condition Type",
        selection=[("hour", "Hours"), ("km", "Kilometers")],
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_instance = fields.Boolean(
        string="Product Instance",
        default=False,
        help="This product is a product instance, which can only have one unit in stock.",
    )

    @api.onchange("product_instance")
    def onchange_product_instance(self):
        if self.product_instance:
            self.tracking = "serial"
            self.type = "product"

    @api.onchange("tracking")
    def onchange_tracking(self):
        res = super(ProductTemplate, self).onchange_tracking()
        products = self.filtered(
            lambda self: self.tracking and self.tracking != "serial"
        )
        if products:
            products.product_instance = False
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    instance_serial_number_id = fields.Many2one(
        "stock.production.lot",
        "Serial Number",
        ondelete="set null",
        domain="[('product_id', '=', id)]",
    )

    instance_current_location_id = fields.Many2one(
        "stock.location", string="Current Location"
    )
    instance_state = fields.Selection(
        string="State",
        selection=[
            ("available", "Available"),
            ("rental", "Rental"),
            ("reserved", "Reserved"),
            ("maintenance", "Maintenance"),
            ("repair", "Repair"),
            ("delivery", "Delivery"),
        ],
        compute="_compute_instance_state",
        search="_search_instance_state",
    )

    show_instance_condition_type = fields.Selection(
        string="Show Instance Condition Type",
        related="categ_id.show_instance_condition_type",
        store=True,
    )

    instance_condition_hour = fields.Float(
        string="Current Hours", compute="_compute_instance_condition"
    )

    instance_condition_km = fields.Float(
        string="Current Kilometers", compute="_compute_instance_condition"
    )

    instance_condition_in_tree = fields.Float(
        string="Current Operating Data", compute="_compute_instance_condition"
    )

    instance_condition_date = fields.Datetime(
        string="Condition Date", compute="_compute_instance_condition"
    )

    instance_next_service_date = fields.Date(string="Next Service")

    real_sale_price = fields.Float(
        string="Real Sale Price",
        help="This is the price at which the product instance was actually sold.",
    )

    real_total_kilometers = fields.Float(
        string="Real Total Kilometers",
        help="This is the mileage the product instance had on sale.",
    )

    real_total_hours = fields.Float(
        string="Real Total Hours",
        help="These are the total operating hours that the product instance had on sale.",
    )

    real_total_rental_time = fields.Float(
        string="Real Total Rental Time",
        help="This is the total rental time for this product instance.",
    )

    instance_operating_data_ids = fields.One2many(
        "instance.operating.data", "instance_id", string="Operating Data"
    )

    def _compute_instance_condition(self):
        for product in self:
            product.instance_condition_km = 0.0
            product.instance_condition_hour = 0.0
            product.instance_condition_in_tree = 0.0
            product.instance_condition_date = False
            for o_data in product.instance_operating_data_ids:
                if not product.instance_condition_date:
                    product.instance_condition_date = o_data.date
                    product.instance_condition_in_tree = o_data.operating_data
                if o_data.date > product.instance_condition_date:
                    product.instance_condition_date = o_data.date
                    product.instance_condition_in_tree = o_data.operating_data
            if product.show_instance_condition_type == "hour":
                product.instance_condition_hour = product.instance_condition_in_tree
            elif product.show_instance_condition_type == "km":
                product.instance_condition_km = product.instance_condition_in_tree

    def _compute_instance_state(self):
        # This function can be extended in other module
        for product in self:
            product.instance_state = "available"

    def _search_instance_state(self, operator, value):
        # This function can be extended in other module
        negative = operator in expression.NEGATIVE_TERM_OPERATORS

        # In case we have no value
        if not value:
            return expression.TRUE_DOMAIN if negative else expression.FALSE_DOMAIN

        if operator in ["in", "not in", "!="]:
            # Do not support for 'in' and 'not in' and '!='
            return expression.TRUE_DOMAIN

        return expression.TRUE_DOMAIN

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        res = super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
        args = args or []
        if name:
            domain = [
                "|",
                ("instance_serial_number_id.name", operator, name),
                ("license_plate", operator, name),
            ]
            record_ids = self._search(
                expression.AND([domain, args]),
                limit=limit,
                access_rights_uid=name_get_uid,
            )
            if record_ids:
                res2 = self.browse(record_ids).name_get()
                return list(set(res + res2))
        return res

    @api.onchange("product_instance")
    def onchange_product_instance(self):
        if self.product_instance:
            self.tracking = "serial"
            self.type = "product"

    @api.onchange("tracking")
    def onchange_tracking(self):
        res = super(ProductProduct, self).onchange_tracking()
        products = self.filtered(
            lambda self: self.tracking and self.tracking != "serial"
        )
        if products:
            products.product_instance = False
        return res

    def action_view_operating_data(self):
        self.ensure_one()
        action = self.env.ref(
            "rental_product_instance.action_instance_operating_data"
        ).read([])[0]
        action["context"] = {
            "default_instance_id": self.id,
            "search_default_instance_id": self.id,
        }
        return action
