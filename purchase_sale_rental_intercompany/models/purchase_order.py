from odoo import _, api, models, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
from odoo.tools import float_round


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
            "start_date": purchase_line.start_date,
            "end_date": purchase_line.end_date,
            "rental": True,
            "product_uom": purchase_line.product_uom.id,
            "price_unit": purchase_line.price_unit,
            "product_uom_qty": purchase_line._get_number_of_time_unit(),
            "number_of_time_unit": purchase_line._get_number_of_time_unit(),
            "rental_qty": purchase_line.product_qty,
            "order_type": "rental",
            "rental_type": "new_rental",
            "display_product_id": purchase_line.product_id.rented_product_id.id,
        })
        return new_line


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    state = fields.Selection(related='order_id.state', store=True, readonly=False, default='draft')

    @api.model
    def _get_time_uom(self):
        uom_month = self.env.ref("rental_base.product_uom_month")
        uom_day = self.env.ref("uom.product_uom_day")
        uom_hour = self.env.ref("uom.product_uom_hour")
        return {
            "month": uom_month,
            "day": uom_day,
            "hour": uom_hour,
        }

    @api.multi
    def _get_number_of_time_unit(self):
        self.ensure_one()
        number = False
        time_uoms = self._get_time_uom()
        if self.product_uom.id == time_uoms["day"].id:
            number = (self.end_date - self.start_date).days + 1
        elif self.product_uom.id == time_uoms["hour"].id:
            number = ((self.end_date - self.start_date).days + 1) * 8
        elif self.product_uom.id == time_uoms["month"].id:
            # ref link to calculate months (why 30.4167 ?)
            # https://www.checkyourmath.com/convert/time/days_months.php
            number = ((self.end_date - self.start_date).days + 1) / 30.4167
            number = float_round(number, precision_rounding=1)
        return number

    @api.onchange("product_id")
    def onchange_product_id(self):
        res = super().onchange_product_id()
        if (
            self.product_id.rental
            and self.product_id.rented_product_id
            and self.product_id.rented_product_id.rental
        ):
            if "domain" in res and "product_uom" in res["domain"]:
                del res["domain"]["product_uom"]
                uom_ids = self.product_id.uom_po_id.ids
                res["domain"]["product_uom"] = [("id", "in", uom_ids)]
                if uom_ids and self.product_uom.id not in uom_ids:
                    self.product_uom = uom_ids[0]
        return res
