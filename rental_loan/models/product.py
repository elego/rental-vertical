# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    loan_count = fields.Integer(
        compute="_compute_loan_count",
        string="Loans",
        help="Total number of Loans",
    )

    def _get_loan_ids(self):
        self.ensure_one()
        loans = self.env["account.loan"].sudo().search([("product_id", "=", self.id)])
        return loans.ids

    def _compute_loan_count(self):
        for rec in self:
            rec.loan_count = len(rec._get_loan_ids())

    def action_view_loan(self):
        self.ensure_one()
        action = self.env.ref("account_loan.account_loan_action").read([])[0]
        action["domain"] = [("id", "in", self._get_loan_ids())]
        context = eval(action["context"])
        context.update(
            {
                "default_product_id": self.id,
                "default_is_leasing": True,
            }
        )
        action["context"] = context
        return action
