# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class AccountIncoterms(models.Model):
    _inherit = "account.incoterms"

    trans_pr_needed = fields.Boolean(
        "Outbound transport required",
        help="If set, this incoterm allows the salesperson to create a transport request or call for tender from a sale order in order to find a carrier delivering the sold products.",
    )
