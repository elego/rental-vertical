# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    toll_line_ids = fields.One2many(
        comodel_name="toll.charge.line",
        inverse_name="invoice_id",
        string="Toll Charge Lines",
    )

    toll_line_count = fields.Integer(
        compute="_compute_toll_line_count",
        string="# Toll Charge Lines",
        type="integer",
    )

    toll_line_charged_count = fields.Integer(
        compute="_compute_toll_charged_count",
        string="# Invoiced Toll Charge Lines",
        type="integer",
    )

    update_toll_lines = fields.Boolean(
        string="Update Toll Charge Lines", compute="_compute_update_toll_lines"
    )

    def _compute_toll_charged_count(self):
        for rec in self:
            rec.toll_line_charged_count = len(rec.toll_line_ids.filtered("invoiced"))

    def _compute_toll_line_count(self):
        for rec in self:
            rec.toll_line_count = len(rec.toll_line_ids)

    def _compute_update_toll_lines(self):
        for rec in self:
            rec.update_toll_lines = any(
                rec.invoice_line_ids.mapped("update_toll_lines")
            )

    def action_view_product_toll_charges(self):
        self.ensure_one()
        tree_view_id = self.env.ref("rental_toll_collect.toll_charge_line_tree_view").id
        form_view_id = self.env.ref("rental_toll_collect.toll_charge_line_form_view").id
        return {
            "type": "ir.actions.act_window",
            "name": _("Toll Charges"),
            "target": "current",
            "view_mode": "tree,form",
            "view_ids": [tree_view_id, form_view_id],
            "res_model": "toll.charge.line",
            "domain": "[('id','in',["
            + ",".join(map(str, self.toll_line_ids.ids))
            + "])]",
        }

    def action_update_toll_charges(self):
        for invoice in self:
            for line in invoice.invoice_line_ids:
                line.update_toll_charge_lines()
                if line.toll_line_ids:
                    if line.toll_product_line_ids:
                        vals = line._prepare_toll_product_line(
                            line.toll_line_ids.filtered("chargeable")
                        )
                        line.toll_product_line_ids.with_context(
                            check_move_validity=False
                        ).write(vals)
                    else:
                        # When manually invoicing toll charge lines,
                        # the 'toll charge' is linked as invoice_line_id.
                        # The 'toll charge' position does not have toll_product_line_ids
                        # and no toll_product_origin_line_id!
                        if (
                            line.product_id
                            == self.env.ref("rental_toll_collect.product_toll")
                            and not line.toll_product_origin_line_id
                        ):
                            vals = self.env[
                                "toll.charge.line.invoicing"
                            ]._prepare_toll_product_line(
                                invoice=invoice,
                                product=line.toll_line_ids.mapped("product_id"),
                                chargeable_toll_lines=line.toll_line_ids.filtered(
                                    "chargeable"
                                ),
                            )
                            line.with_context(check_move_validity=False).write(vals)
                        else:
                            line._create_toll_product_line()
                line.with_context(check_move_validity=False).write(
                    {"update_toll_lines": False}
                )
        return True

    def _get_toll_report_filename(self):
        self.ensure_one()
        if self.state == "draft":
            return _("Toll")
        else:
            return _("Toll - %s") % (self.number)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    toll_line_ids = fields.One2many(
        comodel_name="toll.charge.line",
        inverse_name="invoice_line_id",
        string="Toll Charge Lines",
    )

    toll_product_origin_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Origin for toll product invoice line",
        copy=False,
    )

    toll_product_line_ids = fields.One2many(
        comodel_name="account.move.line",
        inverse_name="toll_product_origin_line_id",
        string="Toll product invoice lines",
    )

    update_toll_lines = fields.Boolean(
        string="Update Toll Charge Lines",
        default=False,
    )

    @api.onchange(
        "product_id",
        "start_date",
        "end_date",
    )
    def onchange_toll_lines_params(self):
        self.update_toll_lines = True

    def _prepare_toll_product_line(self, chargeable_toll_lines):
        self.ensure_one()
        toll_charge_product = self.env.ref("rental_toll_collect.product_toll")
        uom_km = self.env.ref("uom.product_uom_km")
        distance = sum(chargeable_toll_lines.mapped("distance"))
        total_amount = sum(chargeable_toll_lines.mapped("amount"))
        license_plate = (
            self.product_id.license_plate
            or self.product_id.rented_product_id.license_plate
            if self.product_id.rented_product_id
            else ""
        )
        account_id = self._get_computed_account()
        # create invoice line name in partner language
        partner_lang = self.move_id.partner_id.lang
        self.env = api.Environment(
            self.env.cr, self.env.uid, dict(self.env.context, lang=partner_lang)
        )
        name = (
            toll_charge_product.with_context(lang=partner_lang).display_name
            + _(" for ")
            + license_plate
            + _(" Total Distance: ")
            + str(round(distance, 2))
            + " "
            + uom_km.name
        )

        vals = {
            "product_id": toll_charge_product.id,
            "quantity": 1.0,
            "product_uom_id": toll_charge_product.uom_id.id,
            "price_unit": round(total_amount, 2),
            "name": name,
            "toll_product_origin_line_id": self.id,
            "move_id": self.move_id.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "account_id": account_id.id,
            "analytic_account_id": self.analytic_account_id.id
            if self.analytic_account_id
            else False,
        }
        return vals

    def _create_toll_product_line(self):
        self.ensure_one()
        chargeable_toll_lines = self.toll_line_ids.filtered("chargeable")
        values = self._prepare_toll_product_line(chargeable_toll_lines)
        MoveLine = self.env["account.move.line"].with_context(check_move_validity=False)
        toll_product_line = MoveLine.create(values)
        toll_product_line._onchange_product_id()
        toll_product_line.write(
            {
                "price_unit": values.get(
                    "price_unit", toll_product_line.product_id.list_price
                ),
                "name": values.get("name"),
            }
        )
        return toll_product_line

    def _prepare_administrative_product_line(self, invoice, product):
        account_id = self.env["account.move.line"]._get_computed_account()
        vals = {
            "product_id": product.id,
            "quantity": 1.0,
            "uom_id": product.uom_id.id,
            "price_unit": product.list_price,
            "name": product.with_context(lang=invoice.partner_id.lang).display_name,
            "invoice_id": invoice.id,
            "account_id": account_id.id,
            "analytic_account_id": product.income_analytic_account_id
            and product.income_analytic_account_id.id,
        }
        return vals

    def _create_administrative_product_line(self, invoice, charge_product):
        values = self._prepare_administrative_product_line(invoice, charge_product)
        MoveLine = self.env["account.move.line"].with_context(check_move_validity=False)
        invoice_line = MoveLine.create(values)
        invoice_line._onchange_product_id()
        invoice_line.write(
            {"price_unit": values.get("price_unit", invoice_line.product_id.list_price)}
        )

    def update_toll_charge_lines(self):
        self.ensure_one()
        if not self.display_type:
            if self.product_id != self.env.ref("rental_toll_collect.product_toll"):
                rented_product_id = (
                    self.env["product.product"]
                    .browse(self.product_id.id)
                    .rented_product_id
                )
                products = [self.product_id.id]
                if rented_product_id:
                    products.append(rented_product_id.id)
                toll_charge_lines = self.env["toll.charge.line"].search(
                    [
                        ("product_id", "in", products),
                        ("toll_date", ">=", self.start_date),
                        ("toll_date", "<=", self.end_date),
                        "|",
                        ("invoice_line_id", "=", False),
                        ("invoice_line_id", "=", self.id),
                    ]
                )
                self.with_context(check_move_validity=False).write(
                    {
                        "toll_line_ids": [(6, 0, toll_charge_lines.ids)],
                        "update_toll_lines": False,
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        i_lines = super().create(vals_list)
        if self.env.user.company_id.automatic_toll_charge_invoicing:
            toll_product_lines = self.env["account.move.line"].with_context(
                check_move_validity=False
            )
            for line in i_lines:
                line = line.with_context(check_move_validity=False)
                if not vals_list[0].get("toll_line_ids", False):
                    line.update_toll_charge_lines()
                if line.toll_line_ids:
                    toll_product_lines |= line._create_toll_product_line()
                    line.update_toll_lines = False
            i_lines |= toll_product_lines
        return i_lines

    def write(self, values):
        toll_lines = values.get("toll_line_ids", False)
        toll_charge_product = self.filtered(
            lambda l: l.product_id == self.env.ref("rental_toll_collect.product_toll")
        )
        if toll_charge_product:
            # set context to avoid check for Toll Charge product
            self = self.with_context(check_move_validity=False)
        if toll_lines and any([item[2] for item in toll_lines]):
            values.update({"update_toll_lines": True})
        super(AccountMoveLine, self).write(values)
