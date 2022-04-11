# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    contract_type_id = fields.Many2one(
        comodel_name="contract.order.type",
        string="Contract Type",
    )

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        super(AccountInvoice, self)._onchange_partner_id()
        contract_type = (
            self.partner_id.contract_type
            or self.partner_id.commercial_partner_id.contract_type
        )
        if contract_type:
            self.contract_type_id = contract_type

    @api.onchange("contract_type_id")
    def onchange_sale_type_id(self):
        if self.contract_type_id.payment_term_id:
            self.payment_term = self.contract_type_id.payment_term_id.id
        if self.contract_type_id.journal_id:
            self.journal_id = self.contract_type_id.journal_id.id
