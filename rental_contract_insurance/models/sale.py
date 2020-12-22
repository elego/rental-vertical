# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    insurance_origin_line_id = fields.Many2one(
        "sale.order.line",
        copy=False,
    )
    insurance_line_ids = fields.One2many(
        "sale.order.line",
        "insurance_origin_line_id",
    )
    update_insurance_line = fields.Boolean(
        string="Update Insurance Line",
    )
    insurance_product_ids = fields.One2many(
        "insurance.product.sol.info",
        "sol_id",
        string="Insurance Products",
    )
    insurance_entire_time = fields.Boolean(
        "Insurance for entire Time",
        default=True,
    )

    @api.constrains("insurance_product_ids", "product_uom")
    def _check_insurance_product_uom(self):
        for rec in self:
            res = rec.insurance_product_ids.filtered(
                lambda product: product.insurance_product_id.uom_id != rec.product_uom
            )
        if res:
            raise exceptions.ValidationError(
                _(
                    "Uom of the selected Insurance product should be same as the sale order line"
                )
            )

    @api.onchange(
        "product_uom_qty",
        "product_uom",
        "price_unit",
        "insurance_product_ids",
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

    @api.onchange("product_id", "product_uom")
    def onchange_insurance_product_id(self):
        if (
            self.product_id
            and self.rental
            and self.product_id.type == "service"
            and self.product_id.rented_product_id
        ):
            insurance_products = (
                self.product_id.rented_product_id._get_insurance_product(
                    self.product_uom
                )
            )
            vals = [(5, 0, 0)]
            for ins_prod in insurance_products:
                vals.append(
                    (
                        0,
                        0,
                        {
                            "insurance_product_id": ins_prod.insurance_product_id.id,
                            "insurance_type": ins_prod.insurance_type,
                            "insurance_percent": ins_prod.insurance_percent,
                        },
                    )
                )
            self.insurance_product_ids = vals

    @api.onchange(
        "product_uom_qty",
        "product_uom",
        "price_unit",
        "insurance_entire_time",
        "insurance_product_ids",
    )
    def onchange_insurance_params(self):
        self.update_insurance_line = True

    def _prepare_rental_insurance_line(self, product):
        self.ensure_one()
        res = {
            "name": product.name,
            "product_uom_qty": self.product_uom_qty / self.rental_qty,
            "product_uom": self.product_uom.id,
            "product_id": product.id,
            "insurance_origin_line_id": self.id,
            "order_id": self.order_id.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        qty = self.product_uom_qty / self.rental_qty
        if self.insurance_entire_time:
            qty = self.number_of_time_unit
        res["product_uom_qty"] = qty
        return res

    def _create_rental_insurance_line(self, product):
        self.ensure_one()
        vals = self._prepare_rental_insurance_line(product.insurance_product_id)
        insurance_line = self.env["sale.order.line"].create(vals)
        insurance_line.product_id_change()
        insurance_line.write(
            {
                "name": product.insurance_product_id.name,
                "price_unit": product.insurance_price_unit,
            }
        )
        return insurance_line

    @api.multi
    def update_rental_insurance_line(self):
        self.ensure_one()
        old_insurance_lines = self.insurance_line_ids
        for product in self.insurance_product_ids:
            insurance_line = False
            for line in old_insurance_lines:
                if line.product_id == product.insurance_product_id:
                    insurance_line = line
                    old_insurance_lines -= insurance_line
            if not insurance_line:
                insurance_line = self._create_rental_insurance_line(product)
            qty = self.product_uom_qty / self.rental_qty
            if self.insurance_entire_time:
                qty = self.number_of_time_unit
            insurance_line.write(
                {
                    "product_uom_qty": qty,
                    "product_uom": self.product_uom.id,
                    "price_unit": product.insurance_price_unit,
                }
            )
        if old_insurance_lines:
            old_insurance_lines.unlink()
        self.update_insurance_line = False
        return self.insurance_line_ids

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.insurance_product_ids:
            for product in res.insurance_product_ids:
                res._create_rental_insurance_line(product)
            res.update_insurance_line = False
        return res

    @api.multi
    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        res = super(SaleOrderLine, self)._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id
        )
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res[
                    "analytic_account_id"
                ] = rental_product.income_analytic_account_id.id
        return res

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.insurance_origin_line_id:
            if self.insurance_origin_line_id.product_id.income_analytic_account_id:
                rental_product = self.insurance_origin_line_id.product_id
                res[
                    "account_analytic_id"
                ] = rental_product.income_analytic_account_id.id
        return res
