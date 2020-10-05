# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class UpdateSaleLineDate(models.TransientModel):
    _name = "update.sale.line.date"
    _description = "Update Times"

    date_start = fields.Date(
        string='Date Start',
        required=True,
    )

    date_end = fields.Date(
        string='Date End',
        required=True,
    )

    order_id = fields.Many2one(
        'sale.order',
        string="Sale Order",
    )

    all_line = fields.Boolean(
        string="All Lines",
        help="If set, all order lines of this order are "
             "updated with the given dates.",
    )

    from_line = fields.Integer(
        string="From",
        help="In order to update one or several order lines, "
             "please set a number referring to the first order "
             "line that should to be changed.\n"
             "The first line is referenced by 0."
    )

    to_line = fields.Integer(
        string="To",
        help="In order to update one or several order lines, "
             "please set a number referring to the last order "
             "line that should to be changed.\n"
             "The last line is referenced by the total number "
             "of order lines minus 1."
    )

    @api.model
    def default_get(self, fields):
        res = {}
        active_id = self.env.context.get('active_id')
        order = self.env['sale.order'].browse(active_id)
        res.update({
            'order_id': order.id,
            'date_start': order.default_start_date,
            'date_end': order.default_end_date,
            'all_line': True,
            'from_line': 0,
            'to_line': len(order.order_line) - 1,
        })
        return res

    def action_confirm(self):
        self.ensure_one()
        subject = _('Update Date of Sale Order Lines')
        message_body = ''
        message_body += subject
        if self.all_line:
            self.order_id.order_line.update_start_end_date(self.date_start, self.date_end)
            message_body += _(' (All lines): %s - %s') % (self.date_start, self.date_end)
        else:
            if self.from_line > self.to_line:
                raise exceptions.UserError(
                    _("The value in 'To' is less then the value in 'From'.")
                )
            i = 0
            for line in self.order_id.order_line:
                if self.from_line <= i <= self.to_line:
                    line.update_start_end_date(self.date_start, self.date_end)
                i += 1
            message_body += _(' (Lines: %s - %s): %s - %s') % (
                self.from_line, self.to_line, self.date_start, self.date_end
            )
        self.order_id.message_post(body=message_body, subject=subject, message_type='comment')
