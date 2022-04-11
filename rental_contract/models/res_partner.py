# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    contract_type = fields.Many2one(
        comodel_name="contract.order.type",
        string="Contract Subtype",
        company_dependent=True,
    )

    def act_show_contract(self):
        """This opens contract view
        @return: the contract view
        """
        self.ensure_one()
        res = super().act_show_contract()
        res["context"].update(search_default_group_by_type_id=1)
        return res
