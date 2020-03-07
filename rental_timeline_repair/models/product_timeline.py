# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTimeline(models.Model):
    _inherit = 'product.timeline'

    type = fields.Selection(
        selection_add = [
            ('repair', 'Repair'),
        ],
    )

    _maintenance = fields.Boolean(
        compute="_compute_fields",
    )

    @api.multi
    def _compute_fields(self):
        super(ProductTimeline, self)._compute_fields()
        lang = self.env['res.lang'].search([('code', '=', self.env.user.lang)])
        for line in self:
            if line.res_model == 'repair.order':
                obj = self.env[line.res_model].browse(line.res_id)
                line.name = _('r: %s') % obj.partner_id.name if obj.partner_id else obj.name
                line.order_name = obj.name
                line.partner_id = obj.partner_id.id
                line.partner_shipping_address = obj.address_id._display_address()
                currency = self.env.user.company_id.currency_id
                line.amount = '{total} {currency}'.format(
                    total = lang.format('%.2f', obj.amount_untaxed, grouping=True),
                    currency = currency.symbol,
                )

            _maintenance_domain = [
                ('type', '=', 'repair'),
                ('product_id', '=', line.product_id.id),
                ('date_start', '>=', line.date_start),
                ('date_end', '<=', line.date_end),
            ]

            if line.type == 'repair' and not line.maintenance:
                line._maintenance = False
            else:
                bool(self.search(_maintenance_domain))
