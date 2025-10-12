# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    timeline_ids = fields.One2many(
        "product.timeline",
        compute="_compute_timeline_ids",
    )

    date_start = fields.Date(
        string="Date Start",
        help="Please set here the start date of the service or delivery period. "
             "It will be printed on report, together with the given end date.",
    )

    date_end = fields.Date(
        string="Date End",
        help="Please set here the end date of the service or delivery period. "
             "It will be printed on report, together with the given start date.",
    )

    def _compute_timeline_ids(self):
        for order in self:
            domain = [
                ("res_model", "=", order._name),
                ("res_id", "=", order.id),
            ]
            order.timeline_ids = self.env["product.timeline"].search(domain)

    def _prepare_timeline_vals(self):
        self.ensure_one()
        return {
            "type": "repair",
            "date_start": self.date_start,
            "date_end": self.date_end,
            "product_id": self.product_id.id,
            "order_name": self.name,
            "res_model": self._name,
            "res_id": self.id,
            "click_res_model": self._name,
            "click_res_id": self.id,
        }

    def _create_product_timeline(self):
        self.ensure_one()
        if self.product_id.product_instance and self.date_start and self.date_end:
            vals = self._prepare_timeline_vals()
            self.env["product.timeline"].create(vals)

    def _reset_timeline(self, vals):
        for order in self:
            if order.product_id.product_instance:
                if not order.timeline_ids:
                    raise exceptions.UserError(_("No found timelines."))
                if vals.get("date_start", False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.date_start)
                    timelines[0].date_start = vals["date_start"]
                if vals.get("date_end", False):
                    timelines = sorted(
                        order.timeline_ids, key=lambda l: l.date_end, reverse=True
                    )
                    timelines[0].date_end = vals["date_end"]
                if vals.get("product_id", False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.product_id)
                    product = self.env["product.product"].browse(vals["product_id"])
                    timelines[0].product_id = product.id
                if vals.get("name", False):
                    timelines = sorted(order.timeline_ids, key=lambda l: l.order_name)
                    timelines[0].order_name = vals["name"]
            else:
                raise exceptions.UserError(_("No found repaired product."))

    def _timeline_recompute_fields(self):
        for repair in self:
            repair.timeline_ids._compute_fields()

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            rec._create_product_timeline()
        return res

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        keys = {"date_start", "date_end", "product_id", "name"}
        if keys.intersection(vals.keys()):
            reset_orders = self.browse([])
            date_start = vals.get("date_start", False)
            end_Date = vals.get("date_end", False)
            product_id = vals.get("product_id", False)
            name = vals.get("name", False)
            for order in self:
                if date_start and order.date_start != date_start:
                    reset_orders |= order
                if end_Date and order.date_end != end_Date:
                    reset_orders |= order
                if product_id and order.product_id != product_id:
                    reset_orders |= order
                if name and order.name != name:
                    reset_lines |= order
            reset_orders._reset_timeline(vals)
        keys = set(self.env["product.timeline"]._get_depends_fields("repair.order"))
        if keys.intersection(vals.keys()):
            self._timeline_recompute_fields()
        return res

    def unlink(self):
        res = super(PurchaseOrder, self).unlink()
        domain = [
            ("res_model", "=", self._name),
            ("res_id", "in", self.ids),
        ]
        self.env["product.timeline"].search(domain).unlink()
        return res

    def button_cancel(self):
        """
        delete all time lines
        """
        for order in self:
            order.timeline_ids.unlink()
        res = super().button_cancel()
        return res

    def button_draft(self):
        """
        Recreate the timeline objects when setting purchase order to draft state.
        """
        res = super().button_draft()
        for order in self:
            order._create_product_timeline()
        return res
