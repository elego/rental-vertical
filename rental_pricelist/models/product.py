# Part of rental-vertical See LICENSE file for full copyright and licensing details.

import math

from odoo import api, fields, models, exceptions, _
from odoo.tools import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _default_pricelist(self):
        # TODO change default pricelist if country group exist
        return self.env.ref("product.list0").id

    rental_of_month = fields.Boolean(
        "Rented in months",
        copy=False,
    )

    rental_of_day = fields.Boolean(
        "Rented in days",
        copy=False,
    )

    rental_of_hour = fields.Boolean(
        "Rented in hours",
        copy=False,
    )

    product_rental_month_id = fields.Many2one(
        "product.product",
        "Rental Service (Month)",
        ondelete="set null",
        copy=False,
    )

    product_rental_day_id = fields.Many2one(
        "product.product",
        "Rental Service (Day)",
        ondelete="set null",
        copy=False,
    )

    product_rental_hour_id = fields.Many2one(
        "product.product",
        "Rental Service (Hour)",
        ondelete="set null",
        copy=False,
    )

    rental_price_month = fields.Float(
        string="Price / Month",
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_month_id.list_price",
    )

    rental_price_day = fields.Float(
        string="Price / Day",
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_day_id.list_price",
    )

    rental_price_hour = fields.Float(
        string="Price / Hour",
        store=True,
        copy=False,
        readonly=False,
        related="product_rental_hour_id.list_price",
    )

    day_scale_pricelist_item_ids = fields.One2many(
        "product.pricelist.item",
        "day_item_id",
        string="Day Scale Pricelist Items",
        copy=False,
    )

    month_scale_pricelist_item_ids = fields.One2many(
        "product.pricelist.item",
        "month_item_id",
        string="Month Scale Pricelist Items",
        copy=False,
    )

    hour_scale_pricelist_item_ids = fields.One2many(
        "product.pricelist.item",
        "hour_item_id",
        string="Hour Scale Pricelist Items",
        copy=False,
    )

    def_pricelist_id = fields.Many2one(
        "product.pricelist",
        "Default Pricelist",
        default=lambda self: self._default_pricelist(),
    )

    @api.multi
    def _get_rental_service(self, rental_type):
        self.ensure_one()
        if rental_type == "month" and self.product_rental_month_id:
            return self.product_rental_month_id
        elif rental_type == "day" and self.product_rental_day_id:
            return self.product_rental_day_id
        elif rental_type == "hour" and self.product_rental_hour_id:
            return self.product_rental_hour_id
        else:
            raise exceptions.ValidationError(
                _("The product has no related rental services.")
            )

    @api.model
    def _create_rental_service(self, rental_type, product, price=0):
        time_uoms = self.env["sale.order.line"]._get_time_uom()
        uom = False
        if rental_type == "month":
            uom = time_uoms["month"]
        elif rental_type == "day":
            uom = time_uoms["day"]
        elif rental_type == "hour":
            uom = time_uoms["hour"]
        else:
            raise exceptions.ValidationError(_("No found expected Rental Type."))
        values = {
            "hw_product_id": product.id,
            "name": _("Rental of %s (%s)") % (product.name, uom.name),
            "categ_id": product.categ_id.id,
            "copy_image": True,
        }
        res = (
            self.env["create.rental.product"]
            .with_context(active_model="product.product", active_id=product.id)
            .create(values)
            .create_rental_product()
        )
        rental_service = self.browse(res["res_id"])
        rental_service.write(
            {
                "uom_id": uom.id,
                "uom_po_id": uom.id,
                "rental": True,
                "income_analytic_account_id": product.income_analytic_account_id.id,
                "expense_analytic_account_id": product.expense_analytic_account_id.id,
                "list_price": price,
            }
        )
        return rental_service

    @api.multi
    def _update_rental_service_analytic_account(self, vals):
        self.ensure_one()
        analytic_vals = {}
        if "income_analytic_account_id" in vals:
            analytic_vals["income_analytic_account_id"] = vals.get(
                "income_analytic_account_id", False
            )
        if "expense_analytic_account_id" in vals:
            analytic_vals["expense_analytic_account_id"] = vals.get(
                "expense_analytic_account_id", False
            )
        self.rental_service_ids.write(analytic_vals)

    @api.multi
    def _update_rental_service_default_code(self, vals):
        self.ensure_one()
        dc_vals = {}
        if "default_code" in vals:
            rental_product_dc = vals.get("default_code", False)
            rental_service_dc = _("RENT-%s") % rental_product_dc
            dc_vals["default_code"] = rental_service_dc
        self.rental_service_ids.write(dc_vals)

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        for p in self:
            # Create service product automatically
            if vals.get("rental_of_month", False):
                if not p.product_rental_month_id:
                    service_product = self._create_rental_service(
                        "month", p, p.rental_price_month
                    )
                    p.product_rental_month_id = service_product
            if vals.get("rental_of_day", False):
                if not p.product_rental_day_id:
                    service_product = self._create_rental_service(
                        "day", p, p.rental_price_day
                    )
                    p.product_rental_day_id = service_product
            if vals.get("rental_of_hour", False):
                if not p.product_rental_hour_id:
                    service_product = self._create_rental_service(
                        "hour", p, p.rental_price_hour
                    )
                    p.product_rental_hour_id = service_product
            # update analytic account for service product
            if (
                "income_analytic_account_id" in vals
                or "expense_analytic_account_id" in vals
            ):
                p._update_rental_service_analytic_account(vals)
            # update defaul_code of related rental services
            if vals.get("default_code", False) and p.rental_service_ids:
                p._update_rental_service_default_code(vals)
        return res

    @api.model
    def create(self, vals):
        ext_vals = {}
        if vals.get("rental_of_month", False):
            ext_vals["rental_of_month"] = True
            ext_vals["rental_price_month"] = vals.get("rental_price_month")
            del vals["rental_of_month"]
            if "rental_price_month" in vals:
                del vals["rental_price_month"]
        if vals.get("rental_of_day", False):
            ext_vals["rental_of_day"] = True
            ext_vals["rental_price_day"] = vals.get("rental_price_day")
            del vals["rental_of_day"]
            if "rental_price_day" in vals:
                del vals["rental_price_day"]
        if vals.get("rental_of_hour", False):
            ext_vals["rental_of_hour"] = True
            ext_vals["rental_price_hour"] = vals.get("rental_price_hour")
            del vals["rental_of_hour"]
            if "rental_price_hour" in vals:
                del vals["rental_price_hour"]
        res = super().create(vals)
        if "income_analytic_account_id" in vals:
            ext_vals["income_analytic_account_id"] = vals.get(
                "income_analytic_account_id", False
            )
        else:
            ext_vals["income_analytic_account_id"] = res.income_analytic_account_id.id
        if "expense_analytic_account_id" in vals:
            ext_vals["expense_analytic_account_id"] = vals.get(
                "expense_analytic_account_id", False
            )
        else:
            ext_vals["expense_analytic_account_id"] = res.expense_analytic_account_id.id
        res.write(ext_vals)
        return res
