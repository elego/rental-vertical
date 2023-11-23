from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_display_price(self, product):
        no_variant_attributes_price_extra = [
            ptav.price_extra
            for ptav in self.product_no_variant_attribute_value_ids.filtered(
                lambda ptav: ptav.price_extra
                and ptav not in product.product_template_attribute_value_ids
            )
        ]
        if no_variant_attributes_price_extra:
            product = product.with_context(
                no_variant_attributes_price_extra=tuple(
                    no_variant_attributes_price_extra
                )
            )

        if self.order_id.pricelist_id.discount_policy == "with_discount":
            if self.number_of_time_unit:
                return product.with_context(
                    pricelist=self.order_id.pricelist_id.id,
                    uom=self.product_uom.id,
                    quantity=self.number_of_time_unit,
                ).price
            else:
                return product.with_context(
                    pricelist=self.order_id.pricelist_id.id, uom=self.product_uom.id
                ).price

        product_context = dict(
            self.env.context,
            partner_id=self.order_id.partner_id.id,
            date=self.order_id.date_order,
            uom=self.product_uom.id,
        )

        final_price, rule_id = self.order_id.pricelist_id.with_context(
            product_context
        ).get_product_price_rule(
            product or self.product_id,
            self.product_uom_qty or 1.0,
            self.order_id.partner_id,
        )
        base_price, currency = self.with_context(
            product_context
        )._get_real_price_currency(
            product,
            rule_id,
            self.product_uom_qty,
            self.product_uom,
            self.order_id.pricelist_id.id,
        )

        if currency != self.order_id.pricelist_id.currency_id:
            base_price = currency._convert(
                base_price,
                self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.company,
                self.order_id.date_order or fields.Date.today(),
            )
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)
