from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from datetime import timedelta

class RentalPackProductRouteLine(models.TransientModel):
    """
    Setting of routes for sale rental
    """

    _name = "rental.pack.product.route.line"
    _description = "Sale Rental Route In Line"

    product_line_id = fields.Many2one(
        comodel_name="rental.stock.product.line",
        string="Product Line",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        related="product_line_id.product_id",
    )
    qty = fields.Float(
        string="Quantity",
    )
    required_qty = fields.Float(
        string="Required Quantity",
    )
    avail_qty = fields.Float(
        string="Available Quantity",
        compute="compute_avail_qty",
    )

    @api.multi
    def compute_avail_qty(self):
        for rec in self:
            rec.avail_qty = 0
            if rec.product_line_id:
                rec.avail_qty = rec.product_line_id.total_qty_in - rec.product_line_id.routed_qty_in


class RentalPackProductRoute(models.TransientModel):
    """
    Setting of routes for sale rental
    """

    _name = "rental.pack.product.route"
    _description = "Rental Pack Product Route"

    delay = fields.Integer(
        string="Delay",
    )
    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Rental",
        required=True,
    )
    start_date = fields.Date(
        string="Start Date",
        compute="_compute_start_date"
    )
    source_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="From Rental",
    )
    lines = fields.Many2many(
        comodel_name="rental.pack.product.route.line",
        string="Source Products",
    )

    @api.depends("order_id", "delay")
    def _compute_start_date(self):
        for rec in self:
            rec.start_date = rec.order_id.default_start_date - timedelta(days=self.delay)

    @api.model
    def default_get(self, fields):
        model = self._context.get("active_model", False)
        active_id = (
            self._context.get("active_ids", [])
            and self._context.get("active_ids", [])[0]
            or self._context.get("active_id", False)
        )
        res = {}
        res["lines"] = []
        if model == "sale.order" and active_id:
            rental = self.env["sale.order"].browse(active_id)
            if not rental:
                raise UserError(
                    _(
                        "There is no rental object for this position."
                    )
                )
            res["order_id"] = rental.id
        return res

    @api.onchange("source_order_id")
    def onchange_source_order_id(self):
        lines = [(5, 0, 0)]
        for line in self.source_order_id.rental_stock_product_line_ids:
            required_qty = 0
            for dest_line in  self.order_id.rental_stock_product_line_ids:
                if line.product_id.id == dest_line.product_id.id:
                    required_qty = dest_line.out_move_id.product_uom_qty
                    break
            if line.in_move_ids:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "parent_id": self.id,
                            "product_line_id": line.id,
                            "qty": line.total_qty_in - line.routed_qty_in,
                            "required_qty": required_qty,
                        },
                    )
                )
        return {"value": {"lines": lines}}

    @api.multi
    def check_forward_lines(self):
        self.ensure_one()
        for line in self.lines:
            if line.qty > line.avail_qty:
                raise UserError(_("You can not forward more quantities than available."))
        default_start_date = self.source_order_id.default_start_date
        default_end_date = self.source_order_id.default_end_date
        for line in self.source_order_id.order_line:
            if line.start_date != default_start_date or line.end_date != default_end_date:
                raise UserError(_("You can not forward this rental order. Because the start or end dates are not unique in its positions."))
        default_start_date = self.order_id.default_start_date
        default_end_date = self.order_id.default_end_date
        for line in self.order_id.order_line:
            if line.start_date != default_start_date or line.end_date != default_end_date:
                raise UserError(_("You can not define a new route of current rental order. Because the start or end dates are not unique in its positions."))

    @api.multi
    def action_confirm(self):
        """
        Setup Route
        """
        self.ensure_one()
        self.check_forward_lines()
        out_pickings = self.source_order_id.picking_ids.filtered(
            lambda x: x.picking_type_id.code == "incoming" and x.state != "cancel"
        )
        if not out_pickings:
            raise UserError(_("No found Picking for Rental (In)"))
        new_picking = out_pickings[0].copy(
            {
                "move_lines": [],
                "origin": "%s -> %s" %(self.source_order_id.name, self.order_id.name),
                "picking_type_id": self.order_id.warehouse_id.int_type_id.id,
                "location_id": self.source_order_id.partner_shipping_id.rental_onsite_location_id.id,
                "location_dest_id": self.order_id.partner_shipping_id.rental_onsite_location_id.id,
                "rental_order": self.source_order_id.id,
            }
        )
        for product_line in self.order_id.rental_stock_product_line_ids:
            for line in self.lines:
                if product_line.product_id == line.product_id:
                    product_line.forward_product(line.product_line_id, line.qty, new_picking)
                    break
        return True
