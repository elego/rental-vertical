# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    transport_cost_type = fields.Selection(
        selection=[
            ("single", "Single Position"),
            ("multi", "Multi Positions")
        ],
        default="multi",
        string="Transport Cost Type",
        config_parameter="sale.sale_transport_cost_type",
        help="Choosing the cost type 'Multi Positions' the transport "
             "purchase order or call for tender can contain several "
             "lines for the different costs related to the transport, "
             "e.g. the transport costs itself and several charges. "
             "You can define the appropriate transport services when "
             "creating a new transport request.\n"
             "Choosing the cost type 'Single Position' the transport "
             "request will only consist of one line with all costs.",
    )

    transport_cost_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Transport Cost Product",
        domain="[('type', '=', 'service'), ('is_transport', '=', True)]",
        config_parameter="sale.transport_cost_product_id",
        help="This is the default product used for transport costs.",
    )
