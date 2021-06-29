from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class SaleRentalRouteOutLine(models.TransientModel):
    """
    Setting of routes for sale rental
    """

    _name = "sale.rental.route.out.line"
    _description = "Sale Rental Route Out Line"

    parent_id = fields.Many2one("sale.rental.route", "Parent")
    rental_id = fields.Many2one("sale.rental", "Rental", required=True)
    move_id = fields.Many2one("stock.move", "Move", related="rental_id.out_move_id")
    product_id = fields.Many2one(
        "product.product",
        "Product",
        related="rental_id.out_move_id.product_id",
    )
    qty = fields.Float("Rental Quantity")
    rental_avail_qty = fields.Float("Availiable Quantity")
    rental_in_id = fields.Many2one("sale.rental", "Rental (in)")
    rental_in_move_id = fields.Many2one(
        "stock.move", "Move (in)", related="rental_in_id.in_move_id"
    )
    rental_start_date = fields.Date("Rental start date")
    rental_onsite_location_id = fields.Many2one(
        "stock.location", string="source location"
    )

    @api.model
    def default_get(self, fields):
        res = {}
        rental_id = self.env.context.get("rental_id", False)
        if rental_id:
            rental = self.env["sale.rental"].browse(rental_id)
            res["rental_id"] = rental_id
            res["rental_start_date"] = rental.start_date
            res["qty"] = 0
        return res

    @api.multi
    def _split_rental_move(self):
        self.ensure_one()
        if not self.rental_in_id:
            return False
        rounding = self.product_id.uom_id.rounding
        if (
            float_compare(self.rental_avail_qty, self.qty, precision_rounding=rounding)
            < 0
        ):
            raise UserError(
                _(
                    "You can not reorder the Rental, available \
                quantity is less then the required quantity."
                )
            )
        # Moves for rented product use always the default uom of the product.
        # So we don't need to compute the quantity in uom of move.
        self.move_id.product_uom_qty -= self.qty
        new_picking = self.rental_in_move_id.picking_id.copy(
            {
                "move_lines": [],
                "picking_type_id": self.rental_in_id.start_order_line_id.order_id.warehouse_id.int_type_id.id,
                "location_id": self.rental_in_move_id.location_id.id,
                "location_dest_id": self.move_id.location_dest_id.id,
                "rental_order": self.rental_in_id.start_order_line_id.order_id.id,
            }
        )
        reset_qty = False
        if (
            float_compare(
                self.rental_in_move_id.product_qty,
                self.qty,
                precision_rounding=rounding,
            )
            == 0
        ):
            self.rental_in_move_id.product_uom_qty += 1
            reset_qty = True
        new_move_id = self.rental_in_move_id.with_context(
            do_not_push_apply=True
        )._split(self.qty)
        if reset_qty:
            self.rental_in_move_id.product_uom_qty -= 1
        new_move = self.env["stock.move"].browse(new_move_id)
        new_move.write(
            {
                "location_id": self.rental_in_move_id.location_id.id,
                "location_dest_id": self.move_id.location_dest_id.id,
                "rental_in_id": self.rental_in_id.id,
                "rental_out_id": self.rental_id.id,
                "group_id": self.move_id.group_id.id,
                #'procurement_id': self.move_id.procurement_id.id,
                "picking_id": new_picking.id,
            }
        )
        return new_move

    @api.onchange("rental_in_id")
    def onchange_rental_in_id(self):
        if self.rental_in_id:
            if self.rental_in_id.end_date > self.rental_id.start_date:
                raise UserError(
                    _(
                        "The end date of the seleted rental is \
                    later then the start date of current rental."
                    )
                )
            self.rental_avail_qty = self.rental_in_id.in_move_id.product_qty
            self.rental_onsite_location_id = self.rental_in_id.rental_onsite_location_id

    @api.onchange("rental_onsite_location_id")
    def onchange_rental_onsite_location_id(self):
        domain = [
            ("in_move_id.product_qty", ">", 0),
            ("state", "!=", "cancel"),
            ("end_date", "<=", self.rental_start_date),
        ]
        if self.rental_onsite_location_id:
            domain.append(
                (
                    "rental_onsite_location_id",
                    "=",
                    self.rental_onsite_location_id.id,
                )
            )
        return {"domain": {"rental_in_id": domain}}


class SaleRentalRouteInLine(models.TransientModel):
    """
    Setting of routes for sale rental
    """

    _name = "sale.rental.route.in.line"
    _description = "Sale Rental Route In Line"

    parent_id = fields.Many2one("sale.rental.route", "Parent")
    rental_id = fields.Many2one("sale.rental", "Rental", required=True)
    move_id = fields.Many2one("stock.move", "Move", related="rental_id.in_move_id")
    product_id = fields.Many2one(
        "product.product", "Product", related="rental_id.in_move_id.product_id"
    )
    qty = fields.Float("Rental Quantity")
    rental_avail_qty = fields.Float("Required Quantity")
    rental_out_id = fields.Many2one("sale.rental", "Rental (out)")
    rental_out_move_id = fields.Many2one(
        "stock.move", "Move (out)", related="rental_out_id.out_move_id"
    )
    rental_end_date = fields.Date("Rental end date")
    rental_onsite_location_id = fields.Many2one(
        "stock.location", string="dest. location"
    )

    @api.model
    def default_get(self, fields):
        res = {}
        rental_id = self.env.context.get("rental_id", False)
        if rental_id:
            rental = self.env["sale.rental"].browse(rental_id)
            res["rental_id"] = rental_id
            res["rental_end_date"] = rental.end_date
            res["qty"] = 0
        return res

    @api.multi
    def _split_rental_move(self):
        self.ensure_one()
        if not self.rental_out_id:
            return False
        rounding = self.product_id.uom_id.rounding
        if (
            float_compare(self.rental_avail_qty, self.qty, precision_rounding=rounding)
            < 0
        ):
            raise UserError(
                _(
                    "You can not reorder the Rental, \
                available quantity is less then the required quantity."
                )
            )
        # Moves for rented product use always the default uom of the product.
        # So we don't need to compute the quantity in uom of move.
        self.move_id.product_uom_qty -= self.qty
        new_picking = self.move_id.picking_id.copy(
            {
                "move_lines": [],
                "picking_type_id": self.rental_id.start_order_line_id.order_id.warehouse_id.int_type_id.id,
                "location_id": self.move_id.location_id.id,
                "location_dest_id": self.rental_out_move_id.location_dest_id.id,
                "rental_order": self.rental_id.start_order_line_id.order_id.id,
            }
        )
        reset_qty = False
        if (
            float_compare(
                self.rental_out_move_id.product_qty,
                self.qty,
                precision_rounding=rounding,
            )
            == 0
        ):
            self.rental_out_move_id.product_uom_qty += 1
            reset_qty = True
        new_move_id = self.rental_out_move_id.with_context(
            do_not_push_apply=True
        )._split(self.qty)
        if reset_qty:
            self.rental_out_move_id.product_uom_qty -= 1
        new_move = self.env["stock.move"].browse(new_move_id)
        new_move.write(
            {
                "location_id": self.move_id.location_id.id,
                "location_dest_id": self.rental_out_move_id.location_dest_id.id,
                "rental_out_id": self.rental_out_id.id,
                "rental_in_id": self.rental_id.id,
                "group_id": self.rental_out_move_id.group_id.id,
                #'procurement_id': self.rental_out_move_id.procurement_id.id,
                "picking_id": new_picking.id,
            }
        )
        return new_move

    @api.onchange("rental_out_id")
    def onchange_rental_out_id(self):
        if self.rental_out_id:
            if self.rental_out_id.start_date < self.rental_id.end_date:
                raise UserError(
                    _(
                        "The start date of the seleted rental \
                    is earlier then the end date of current rental."
                    )
                )
            self.rental_avail_qty = self.rental_out_id.out_move_id.product_qty
            self.rental_onsite_location_id = (
                self.rental_out_id.rental_onsite_location_id
            )

    @api.onchange("rental_onsite_location_id")
    def onchange_rental_onsite_location_id(self):
        domain = [
            ("out_move_id.product_qty", ">", 0),
            ("state", "!=", "cancel"),
            ("start_date", ">=", self.rental_end_date),
        ]
        if self.rental_onsite_location_id:
            domain.append(
                (
                    "rental_onsite_location_id",
                    "=",
                    self.rental_onsite_location_id.id,
                )
            )
        return {"domain": {"rental_out_id": domain}}


class SaleRentalRoute(models.TransientModel):
    """
    Setting of routes for sale rental
    """

    _name = "sale.rental.route"
    _description = "Sale Rental Route"

    rental_id = fields.Many2one("sale.rental", "Rent")
    product_id = fields.Many2one(
        "product.product", related="rental_id.rented_product_id"
    )
    out_lines = fields.One2many(
        "sale.rental.route.out.line", "parent_id", "Route (Out)"
    )
    in_lines = fields.One2many(
        "sale.rental.route.in.line", "parent_id", "Route (Return)"
    )

    @api.model
    def default_get(self, fields):
        model = self._context.get("active_model", False)
        active_id = (
            self._context.get("active_ids", [])
            and self._context.get("active_ids", [])[0]
            or self._context.get("active_id", False)
        )
        res = {}
        res["out_lines"] = []
        res["in_lines"] = []
        if model == "sale.order.line" and active_id:
            rentals = self.env["sale.rental"].search(
                [("start_order_line_id", "=", active_id)]
            )
            if not rentals:
                raise UserError(
                    _(
                        "Do not find the rental \
                    object of this position."
                    )
                )
            res["rental_id"] = rentals[0].id
            if rentals[0].out_move_id and rentals[0].out_move_id.product_qty > 0:
                res["out_lines"].append(
                    (
                        0,
                        0,
                        {
                            "rental_id": rentals[0].id,
                            "rental_start_date": rentals[0].start_date,
                            "qty": rentals[0].out_move_id.product_qty,
                        },
                    )
                )
            if rentals[0].in_move_id and rentals[0].in_move_id.product_qty > 0:
                res["in_lines"].append(
                    (
                        0,
                        0,
                        {
                            "rental_id": rentals[0].id,
                            "rental_end_date": rentals[0].end_date,
                            "qty": rentals[0].in_move_id.product_qty,
                        },
                    )
                )
            # if not res['out_lines'] or not res['in_lines']:
            #    raise UserError(_("No out lines or in lines was found."))
        return res

    @api.multi
    def _check_route_lines(self):
        self.ensure_one()
        out_qty_sum = 0
        out_dic = {}
        in_qty_sum = 0
        in_dic = {}
        for line in self.out_lines:
            out_qty_sum += line.qty
            if line.rental_in_id:
                if line.rental_in_id not in out_dic:
                    out_dic[line.rental_in_id] = line.qty
                else:
                    out_dic[line.rental_in_id] += line.qty
        for line in self.in_lines:
            in_qty_sum += line.qty
            if line.rental_out_id:
                if line.rental_out_id not in in_dic:
                    in_dic[line.rental_out_id] = line.qty
                else:
                    in_dic[line.rental_out_id] += line.qty
        rounding = self.rental_id.rented_product_id.uom_id.rounding
        if (
            float_compare(
                self.rental_id.out_move_id.product_uom_qty,
                out_qty_sum,
                precision_rounding=rounding,
            )
            < 0
        ):
            raise UserError(
                _(
                    'You have assigned more qty \
                than requried for "Route (Out)".'
                )
            )
        if (
            float_compare(
                self.rental_id.in_move_id.product_uom_qty,
                in_qty_sum,
                precision_rounding=rounding,
            )
            < 0
        ):
            raise UserError(
                _(
                    'You have assigned more qty \
                than requried for "Route (Return)".'
                )
            )
        for r, qty in out_dic.items():
            if qty > r.in_move_id.product_uom_qty:
                raise UserError(
                    _(
                        'You have assigned more qty \
                    than available from "%s".'
                    )
                    % r.display_name
                )
        for r, qty in in_dic.items():
            if qty > r.out_move_id.product_uom_qty:
                raise UserError(
                    _(
                        'You have assigned more qty \
                    than available from "%s".'
                    )
                    % r.display_name
                )

    @api.multi
    def action_confirm(self):
        """
        Setup Route
        """
        self.ensure_one()
        self._check_route_lines()
        for l in self.out_lines:
            if l.rental_in_id:
                l._split_rental_move()
        for l in self.in_lines:
            if l.rental_out_id:
                l._split_rental_move()
        return True
