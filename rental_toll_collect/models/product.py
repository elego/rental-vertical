# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    toll_line_ids = fields.One2many(
        comodel_name="toll.charge.line",
        inverse_name="product_id",
        string="Toll Charge Lines",
        help="These are all toll charge lines related to this product.",
    )

    toll_amount = fields.Monetary(
        string="Open Toll Charges",
        help="This is the total amount of not yet invoiced toll charges for this product.",
        compute="_compute_open_toll_charges_amount",
        store=True,
        readonly=True,
        tracking=True,
    )

    open_toll_charge_count = fields.Integer(
        string="# Open Toll Charge Lines",
        help="This is the number of not yet invoiced toll charge lines related"
        " to this product.",
        compute="_compute_open_toll_charges_count",
        type="integer",
    )

    @api.depends(
        "toll_line_ids.amount", "toll_line_ids.invoiced", "toll_line_ids.chargeable"
    )
    def _compute_open_toll_charges_count(self):
        for rec in self:
            rec.open_toll_charge_count = len(
                rec.toll_line_ids.filtered(lambda x: not x.invoiced and x.chargeable)
            )

    @api.depends(
        "toll_line_ids.amount", "toll_line_ids.invoiced", "toll_line_ids.chargeable"
    )
    def _compute_open_toll_charges_amount(self):
        for rec in self:
            rec.toll_amount = sum(
                rec.toll_line_ids.filtered(
                    lambda x: not x.invoiced and x.chargeable
                ).mapped("amount")
            )

    def action_view_open_toll_charge(self):
        self.ensure_one()
        action = self.env.ref("rental_toll_collect.toll_charge_line_action").read([])[0]
        action["domain"] = [("id", "in", self.toll_line_ids.ids)]
        return action
