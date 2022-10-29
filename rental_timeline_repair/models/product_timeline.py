# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTimeline(models.Model):
    _inherit = "product.timeline"

    type = fields.Selection(
        selection_add=[
            ("repair", "Repair Order"),
        ],
    )

    repair = fields.Boolean(
        string="Repair Order",
        compute="_compute_fields",
        store=True,
    )

    @api.depends("res_id", "res_model")
    def _compute_fields(self):
        super(ProductTimeline, self)._compute_fields()
        lang = self.env["res.lang"].search([("code", "=", self.env.user.company_id.partner_id.lang)])
        for line in self:
            if line.res_model == "repair.order":
                obj = self.env[line.res_model].browse(line.res_id).with_context(lang=lang.code)
                line.name = obj.partner_id.commercial_partner_id.name if obj.partner_id else obj.name
                line.order_name = obj.name
                line.partner_id = obj.partner_id.id
                line.partner_shipping_id = obj.address_id.id
                line.partner_shipping_address = obj.address_id._display_address()
                currency = self.env.user.company_id.currency_id
                line.amount = "{total} {currency}".format(
                    total=lang.format("%.2f", obj.amount_untaxed, grouping=True),
                    currency=currency.symbol,
                )

            if line.type != "repair":
                domain = [
                    ("type", "=", "repair"),
                    ("product_id", "=", line.product_id.id),
                    ("date_start", ">=", line.date_start),
                    ("date_end", "<=", line.date_end),
                ]
                if bool(self.search(domain)):
                    line.repair = True
                    line.has_clues = True

    @api.model
    def _get_depends_fields(self, model):
        res = super()._get_depends_fields(model)
        if model == "repair.order":
            res += [
                "name",
                "partner_id",
                "address_id",
                "amount_untaxed",
            ]
        return res
