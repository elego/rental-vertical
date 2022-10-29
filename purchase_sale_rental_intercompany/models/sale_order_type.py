from odoo import _, api, models, fields
import logging

_logger = logging.getLogger(__name__)


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'

    rel_purchase_order_type_id = fields.Many2one("purchase.order.type",
        string="Related Purchase Order Type",
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args += ['|',('company_id','=',False),('company_id','child_of',[self.env.user.company_id.id])]
        res = super(SaleOrderType, self).search(
            args, offset=offset, limit=limit, order=order, count=count
        )
        return res