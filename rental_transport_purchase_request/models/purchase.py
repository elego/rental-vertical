# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    trans_origin_sale_line_id = fields.Many2one('sale.order.line')
    name = fields.Char('Name')

    @api.multi
    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(
            name=name, product_qty=product_qty, price_unit=price_unit, taxes_ids=taxes_ids)
        res['trans_origin_sale_line_id'] = self.trans_origin_sale_line_id.id
        res['name'] = self.name
        res['date_planned'] = fields.Datetime.to_datetime(self.schedule_date)
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    trans_origin_sale_line_id = fields.Many2one('sale.order.line')
