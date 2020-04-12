# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tranport_cost_type = fields.Selection(
        [
            ('single', 'Single Position'),
            ('multi', 'Multi Positions')
        ],
        default='multi',
        string="Transport Cost Type",
        config_parameter='sale.sale_transport_cost_type',
    )
    transport_cost_product_id = fields.Many2one(
        'product.product',
        'Transport Cost Product',
        domain="[('type', '=', 'service'), ('is_transport', '=', True)]",
        config_parameter='sale.transport_cost_product_id',
        help='Default product used for Transport Cost'
    )
