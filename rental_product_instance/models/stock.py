# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.constrains("product_id", "name")
    def _check_unique_product_instance(self):
        for rec in self:
            if rec.product_id.product_instance:
                domain = [
                    ("product_id", "=", rec.product_id.id),
                    ("id", "!=", rec.id),
                ]
                res = self.search_count(domain)
                if res:
                    msg = _("You can not have 2 serial numbers for a product instance.")
                    raise exceptions.ValidationError(msg)


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        super(StockMove, self).write(vals)
        if vals.get("state", False) == "done":
            for m in self:
                if m.product_id.product_instance:
                    m.product_id.instance_current_location_id = m.location_dest_id
