from odoo import _, api, models, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _prepare_purchase_order_data(self, name, partner, dest_company):
        self.ensure_one()
        new_po = super(SaleOrder, self)._prepare_sale_order_data(name, partner, dest_company)
        if not self.type_id.rel_purchase_order_type_id and self.partner_id.company_type == 'company':
            raise UserError(_("Please choose a sale order type that is configured to match a purchase order type of this supplier."))
        else:
            new_po.update({
                'order_type': self.type_id.rel_purchase_order_type_id.id,
            })
        return new_po

    @api.model
    def _prepare_purchase_order_line_data(
            self, sale_line, purchase_order):
        new_line = super(SaleOrder, self)._prepare_purchase_order_line_data(sale_line, purchase_order)
        new_line.update({
            'start_date': sale_line.start_date,
            'end_date': sale_line.end_date,
        })
        return new_line
