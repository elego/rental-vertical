# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_all_picking_ids(self):
        res = {}
        for sale in self:
            res[sale.id] = []
            # pickings of rental in
            rental_pickings = self.env["stock.picking"].search(
                [("rental_order", "=", sale.id)]
            )
            if rental_pickings:
                res[sale.id] += rental_pickings.ids
            res[sale.id] = list(set(res[sale.id]))
            # search by procurement.group if we found
            # no pickings by procurement.order
            group_picking = []
            if not sale.procurement_group_id:
                continue
            group_picking = (
                self.env["stock.picking"]
                .search([("group_id", "=", sale.procurement_group_id.id)])
                .ids
                if sale.procurement_group_id
                else []
            )
            res[sale.id] = list(
                set(res[sale.id]) | set(group_picking) | set(sale.picking_ids.ids)
            )
        return res

    @api.depends("procurement_group_id")
    def _compute_picking_ids(self):
        picking_dic = self._get_all_picking_ids()
        for sale in self:
            sale.delivery_count = len(picking_dic[sale.id])

    def action_view_delivery(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        picking_ids = self._get_all_picking_ids()[self.id]
        if len(picking_ids) > 1:
            action["domain"] = [("id", "in", picking_ids)]
        elif picking_ids:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = picking_ids[0]
        return action

    def action_confirm(self):
        rental_order_type = self.env.ref("rental_base.rental_sale_type")
        for sale in self:
            if sale.type_id.id == rental_order_type.id:
                if (
                    sale.partner_shipping_id
                    and not sale.partner_shipping_id.rental_onsite_location_id
                ):
                    sale.create_and_set_rental_onsite_location_route()
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            for line in sale.order_line:
                line._reset_forward_rental_source()
        return res

    def action_cancel(self):
        for sale in self:
            rental_pickings = self.env["stock.picking"].search(
                [("rental_order", "=", sale.id)]
            )
            rental_pickings.action_cancel()
        res = super(SaleOrder, self).action_cancel()

    def create_and_set_rental_onsite_location_route(self):
        """
        This function creates the onsite location for the selected
        partner address and its rental route automatically.
        """
        self.ensure_one()
        # create a internal location for partner_shipping_id
        if not self.partner_shipping_id:
            raise UserError(_("There is no shipping address found."))
        partner = self.partner_shipping_id
        if not self.warehouse_id.rental_allowed:
            raise UserError(_("The selected warehouse is not allowed for rental."))
        if not self.warehouse_id.rental_route_id:
            raise UserError(_("There is no default rental route found for the selected warehouse."))
        rental_route = self.warehouse_id.rental_route_id
        if not self.warehouse_id.rental_out_location_id:
            raise UserError(_("There is no Rental Out location found for the selected warehouse."))
        rental_out_location = self.warehouse_id.rental_out_location_id
        if not self.warehouse_id.rental_in_location_id:
            raise UserError(_("There is no Rental In location found for the selected warehouse."))
        rental_in_location = self.warehouse_id.rental_in_location_id
        if not self.warehouse_id.int_type_id:
            raise UserError(_("There is no default picking type 'Internal' found for the selected warehouse."))
        location_name = "Location [%s]" % self.partner_shipping_id.display_name
        new_location = rental_out_location.copy({"name": location_name})

        # set onsite location of partner address
        self.partner_shipping_id.rental_onsite_location_id = new_location

        # Create a new route for the new location
        route_name = "Rent [%s]" % self.partner_shipping_id.display_name
        new_route = self.warehouse_id.rental_route_id.copy({"name": route_name})
        # new_push_rule = new_route.push_ids[0]
        # new_pull_rule = new_route.pull_ids[0]
        for rule in new_route.rule_ids:
            if rule.location_src_id == self.warehouse_id.rental_out_location_id:
                rule.write(
                    {
                        "location_src_id": new_location.id,
                        # "picking_type_id": self.warehouse_id.int_type_id.id,
                    }
                )
            if rule.location_id == self.warehouse_id.rental_out_location_id:
                rule.write(
                    {
                        "location_id": new_location.id,
                        # "picking_type_id": self.warehouse_id.int_type_id.id,
                    }
                )
        self.partner_shipping_id.rental_onsite_location_route = new_route
