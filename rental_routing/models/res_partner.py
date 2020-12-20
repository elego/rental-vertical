# @author Yu Weng <yweng@elegosoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    rental_onsite_location_id = fields.Many2one(
        "stock.location", "Rental Onsite Location", ondelete="set null"
    )
    rental_onsite_location_route = fields.Many2one(
        "stock.location.route",
        "Rental Onsite Location Route",
        ondelete="set null",
    )
