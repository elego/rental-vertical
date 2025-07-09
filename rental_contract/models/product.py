# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    cust_contract_count = fields.Integer(
        compute="_compute_cust_contract_count",
        string="C-Contracts",
        help="Total number of Customer Contracts",
    )
    ven_contract_count = fields.Integer(
        compute="_compute_ven_contract_count",
        string="V-Contracts",
        help="Total number of Vendor/Supplier Contracts",
    )

    @api.onchange("is_contract", "rental")
    def onchange_is_contract_rental(self):
        template = self.env.ref("rental_contract.rental_contract_template")
        if self.is_contract and self.rental:
            self.property_contract_template_id = template.id

    def _get_contract_ids(self, contract_type):
        self.ensure_one()
        cls = self.env["contract.line"].search(
            [
                "|",
                ("product_id", "=", self.id),
                (
                    "product_id",
                    "in",
                    self.search(
                        [
                            "|",
                            "&",
                            ("active", "=", True),
                            ("active", "=", False),
                            ("rented_product_id", "=", self.id),
                        ]
                    ).ids,
                ),
            ]
        )
        return list(
            {
                l.contract_id.id
                for l in cls
                if l.contract_id.contract_type == contract_type
            }
        )

    def action_view_supplier_contract(self):
        self.ensure_one()
        record_ids = self._get_contract_ids(contract_type="purchase")
        action = self.env.ref("contract.action_supplier_contract").read([])[0]
        action["domain"] = [("id", "in", record_ids)]
        return action

    def action_view_customer_contract(self):
        self.ensure_one()
        record_ids = self._get_contract_ids(contract_type="sale")
        action = self.env.ref("contract.action_customer_contract").read([])[0]
        action["domain"] = [("id", "in", record_ids)]
        return action

    def _compute_cust_contract_count(self):
        contract_type = "sale"
        for rec in self:
            rec.cust_contract_count = len(rec._get_contract_ids(contract_type))

    def _compute_ven_contract_count(self):
        contract_type = "purchase"
        for rec in self:
            rec.ven_contract_count = len(rec._get_contract_ids(contract_type))
