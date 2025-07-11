# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ContractOrderType(models.Model):
    _name = "contract.order.type"
    _description = "Contract Subtype"

    @api.model
    def _get_domain_sequence_id(self):
        seq_type = self.env.ref("rental_contract.seq_customer_contract")
        return [("code", "=", seq_type.code)]

    def _default_journal_id(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        return journal.id

    def _default_pricelist_id(self):
        return self.env.ref("product.list0").id

    def _default_payment_term_id(self):
        return self.env.ref("account.account_payment_term_immediate").id

    name = fields.Char(string="Name", required=True, translate=True)
    contract_type = fields.Selection(
        selection=[("sale", "Customer"), ("purchase", "Supplier")],
        default="sale",
        string="Contract Type",
    )
    # you can add more sub types selection values
    # like transport,insurance or whatever
    sub_type = fields.Selection([("rental", "Rental")], "Sub Type")
    description = fields.Text(string="Description", translate=True)
    sequence_id = fields.Many2one(
        "ir.sequence",
        string="Entry Sequence",
        copy=False,
        domain=_get_domain_sequence_id,
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Billing Journal",
        default=lambda self: self._default_journal_id(),
    )
    company_id = fields.Many2one(
        "res.company",
        store=True,
        default=lambda self: self.env.user.company_id.id,
        readonly=True,
    )
    payment_term_id = fields.Many2one(
        "account.payment.term",
        string="Payment Term",
        default=lambda self: self._default_payment_term_id(),
    )
    pricelist_id = fields.Many2one(
        "product.pricelist",
        "Pricelist",
        default=lambda self: self._default_pricelist_id(),
    )

    @api.multi
    @api.onchange("contract_type")
    def onchange_contract_type(self):
        if self.contract_type:
            if self.contract_type == "purchase":
                journal = self.env["account.journal"].search(
                    [("type", "=", "purchase")], limit=1
                )
                self.journal_id = journal.id
                self.sequence_id = self.env.ref(
                    "rental_contract.seq_vendor_contract"
                ).id
            if self.contract_type == "sale":
                journal = self.env["account.journal"].search(
                    [("type", "=", "sale")], limit=1
                )
                self.journal_id = journal.id
                self.sequence_id = self.env.ref(
                    "rental_contract.seq_customer_contract"
                ).id
