from odoo import _, api, models, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _prepare_sale_order_data(self, name, partner, dest_company,
                                 direct_delivery_address):
        self.ensure_one()
        new_so = super(PurchaseOrder, self)._prepare_sale_order_data(name, partner, dest_company, direct_delivery_address)
        if not self.order_type.rel_sale_order_type_id and self.partner_id.company_type == 'company':
            raise UserError(_("Please choose a purchase order type that is configured to match a sale order type of this supplier."))
        else:
            new_so.update({
                # 'default_start_date': self.default_start_date,
                # 'default_end_date': self.default_end_date,
                'type_id': self.order_type.rel_sale_order_type_id.id,
            })
        return new_so

    @api.model
    def _prepare_sale_order_line_data(
            self, purchase_line, dest_company, sale_order):
        new_line = super(PurchaseOrder, self)._prepare_sale_order_line_data(purchase_line, dest_company, sale_order)
        new_line.update({
            'start_date': purchase_line.start_date,
            'end_date': purchase_line.end_date,
        })
        return new_line


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    state = fields.Selection(related='order_id.state', store=True, readonly=False, default='draft')
