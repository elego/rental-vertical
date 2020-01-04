# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rent_ok = fields.Boolean(string='Rent OK') # for rent only
    sell_rent = fields.Boolean(string="Sell Rent") # for selling renatl product only
    rental_uom_id = fields.Many2one('uom.uom', string='Rental Unit of Measure')

    @api.constrains(
        'rental_type', 'extension_rental_id', 'start_date', 'end_date',
        'rental_qty', 'product_uom_qty', 'product_id')
    def _check_sale_line_rental(self):
        for line in self:
            if line.rental_type == 'rental_extension':
                if not line.extension_rental_id:
                    raise ValidationError(_(
                        "Missing 'Rental to Extend' on the sale order line "
                        "with rental service %s") % line.product_id.name)

                if line.rental_qty != line.extension_rental_id.rental_qty:
                    raise ValidationError(_(
                        "On the sale order line with rental service %s, "
                        "you are trying to extend a rental with a rental "
                        "quantity (%s) that is different from the quantity "
                        "of the original rental (%s). This is not supported.")
                        % (
                        line.product_id.name,
                        line.rental_qty,
                        line.extension_rental_id.rental_qty))
            if line.rental_type in ('new_rental', 'rental_extension'):
                # if not line.product_id.rented_product_id:
                #     raise ValidationError(_(
                #         "On the 'new rental' sale order line with product "
                #         "'%s', we should have a rental service product !") % (
                #         line.product_id.name))
                if line.product_uom_qty !=\
                        line.rental_qty * line.number_of_days:
                    raise ValidationError(_(
                        "On the sale order line with product '%s' "
                        "the Product Quantity (%s) should be the "
                        "number of days (%s) "
                        "multiplied by the Rental Quantity (%s).") % (
                        line.product_id.name, line.product_uom_qty,
                        line.number_of_days, line.rental_qty))
                # the module sale_start_end_dates checks that, when we have
                # must_have_dates, we have start + end dates
            elif line.sell_rental_id:
                if line.product_uom_qty != line.sell_rental_id.rental_qty:
                    raise ValidationError(_(
                        "On the sale order line with product %s "
                        "you are trying to sell a rented product with a "
                        "quantity (%s) that is different from the rented "
                        "quantity (%s). This is not supported.") % (
                        line.product_id.name,
                        line.product_uom_qty,
                        line.sell_rental_id.rental_qty))

    @api.onchange('rent_ok')
    def onchange_rent_ok(self):
        if self.rent_ok:
            self.can_sell_rental = False
            self.rental = True
            self.sell_rental_id = False
            if not self.rental_type:
                self.rental_type = 'new_rental'
        else:
            self.rental_type = False
            self.rental = False
            self.rental_qty = 0
            self.extension_rental_id = False
            self.can_sell_rental = False
            #self.sell_rental_id = False

    @api.onchange('sell_rent')
    def onchange_sell_rent(self):
        if self.sell_rent:
            self.rent_ok = False
            self.rental_type = False
            self.rental = False
            self.rental_qty = 0
            self.extension_rental_id = False
            self.can_sell_rental = True
        # else:
        #     self.rental_type = False
        #     self.rental = False
        #     self.rental_qty = 0
        #     self.extension_rental_id = False
        #     self.can_sell_rental = False
        #     self.sell_rental_id = False

    @api.multi
    @api.onchange('product_id', 'rental_qty')
    def rental_product_id_change(self):
        rental_qty = 0.0
        rental_type = False
        extension_rental_id = False
        can_sell_rental = False
        if self.rental_qty:
            rental_qty = self.rental_qty
        if self.rental_type:
            rental_type = self.rental_type
        if self.extension_rental_id:
            extension_rental_id = self.extension_rental_id
        if self.can_sell_rental:
            can_sell_rental = self.can_sell_rental
        res = super().rental_product_id_change()
        self.rental_type = rental_type
        self.extension_rental_id = extension_rental_id
        self.can_sell_rental = can_sell_rental
        day_uom_id = self.env.ref('uom.product_uom_day').id
        if self.product_id:
            if self.rent_ok:
                self.can_sell_rental = False
                self.rental = True
                self.sell_rental_id = False
                self.rental_qty = rental_qty
                self.rental_uom_id = self.product_id.rental_uom_id
                if not self.product_id.must_have_dates:
                    raise UserError(_('Field "Must have Start and Date" on Product must be True'))
                if self.product_id.rental_uom_id.id != day_uom_id:
                    raise UserError(_('Product Rental Unit of Measure must be day(s)'))
                if not self.rental_type:
                    self.rental_type = 'new_rental'
                if (self.rental_type == 'new_rental' and self.rental_qty and self.order_id.warehouse_id):
                    product_uom = self.product_id.uom_id
                    warehouse = self.order_id.warehouse_id
                    rental_in_location = warehouse.rental_in_location_id
                    rented_product_ctx = \
                        self.with_context(
                            location=rental_in_location.id
                        ).product_id
                    in_location_available_qty =\
                        rented_product_ctx.qty_available -\
                        rented_product_ctx.outgoing_qty
                    compare_qty = float_compare(
                        in_location_available_qty, self.rental_qty,
                        precision_rounding=product_uom.rounding)
                    if compare_qty == -1:
                        res['warning'] = {
                            'title': _("Not enough stock !"),
                            'message': _(
                                "You want to rent %.2f %s but you only "
                                "have %.2f %s currently available on the "
                                "stock location '%s' ! Make sure that you "
                                "get some units back in the mean time or "
                                "re-supply the stock location '%s'.") % (
                                self.rental_qty,
                                product_uom.name,
                                in_location_available_qty,
                                product_uom.name,
                                rental_in_location.name,
                                rental_in_location.name)
                        }
            elif self.sell_rent:
                self.can_sell_rental = True
                self.rental = False
                self.rental_type = False
                self.rental_qty = 0
                self.extension_rental_id = False
            else:
                self.rental_type = False
                self.rental = False
                self.rental_qty = 0
                self.extension_rental_id = False
                self.can_sell_rental = False
                self.sell_rental_id = False
        else:
            self.rental_type = False
            self.rental = False
            self.rental_qty = 0
            self.extension_rental_id = False
            self.can_sell_rental = False
            self.sell_rental_id = False
        return res

    def _action_launch_stock_rule(self):
        # replaced method of sale_rental module
        errors = []
        for line in self:
            if (
                    line.rental_type == 'new_rental' and
                    line.rent_ok):
                group = line.order_id.procurement_group_id
                if not group:
                    group = self.env['procurement.group'].create({
                        'name': line.order_id.name,
                        'move_type': line.order_id.picking_policy,
                        'sale_id': line.order_id.id,
                        'partner_id': line.order_id.partner_shipping_id.id,
                    })
                    line.order_id.procurement_group_id = group

                vals = line._prepare_new_rental_procurement_values(group)
                try:
                    self.env['procurement.group'].run(
                        line.product_id, line.rental_qty,
                        line.product_id.uom_id,
                        line.order_id.warehouse_id.rental_out_location_id,
                        line.name, line.order_id.name, vals)
                except UserError as error:
                    errors.append(error.name)

                self.env['sale.rental'].create(line._prepare_rental())
                line.procurement_jit_rental()
                return True

            elif (
                    line.rental_type == 'rental_extension' and
                    line.rent_ok and
                    line.extension_rental_id and
                    line.extension_rental_id.in_move_id):
                end_datetime = fields.Datetime.to_datetime(
                    line.end_date)
                line.extension_rental_id.in_move_id.write({
                    'date_expected': end_datetime,
                    'date': end_datetime,
                    })
                line.procurement_jit_rental()
                return True
            elif line.sell_rental_id:
                if line.sell_rental_id.out_move_id.state != 'done':
                    raise UserError(_(
                        'Cannot sell the rental %s because it has '
                        'not been delivered')
                        % line.sell_rental_id.display_name)
                line.sell_rental_id.in_move_id._action_cancel()

        if errors:
            raise UserError('\n'.join(errors))
        # call super() at the end, to make procurement_jit work
        res = super(SaleOrderLine, self)._action_launch_stock_rule()
        return res

    def procurement_jit_rental(self):
        orders = list(set(x.order_id for x in self))
        for order in orders:
            reassign = order.picking_ids.filtered(lambda x: x.state=='confirmed' or (x.state in ['waiting', 'assigned'] and not x.printed))
            if reassign:
                reassign.action_assign()
        return True

    @api.onchange('rental_qty', 'number_of_days', 'product_id')
    def rental_qty_number_of_days_change(self):
        res = super().rental_qty_number_of_days_change()
        if self.product_id and self.rent_ok:
            qty = self.rental_qty * self.number_of_days
            self.product_uom_qty = qty
        return res

    @api.onchange('extension_rental_id')
    def extension_rental_id_change(self):
        res = super().extension_rental_id_change()
        if self.product_id and\
                self.rental_type == 'rental_extension' and\
                self.extension_rental_id and self.rent_ok:
            if self.extension_rental_id.rental_product_id != self.product_id:
                raise UserError(_(
                    "The Rental Service of the Rental Extension you just "
                    "selected is '%s' and it's not the same as the "
                    "Product currently selected in this Sale Order Line.")
                    % self.extension_rental_id.rental_product_id.name)
            initial_end_date = self.extension_rental_id.end_date
            self.start_date = initial_end_date + relativedelta(days=1)
            self.rental_qty = self.extension_rental_id.rental_qty
        return res