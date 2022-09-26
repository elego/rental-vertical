from odoo import _, api, models, fields
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderType(models.Model):
    _inherit = 'purchase.order.type'

    rel_sale_order_type_id = fields.Many2one("sale.order.type",
        string="Related Sale Order Type",
    )
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args += ['|',('company_id','=',False),('company_id','child_of',[self.env.user.company_id.id])]
        res = super(PurchaseOrderType, self).search(
            args, offset=offset, limit=limit, order=order, count=count
        )
        return res
