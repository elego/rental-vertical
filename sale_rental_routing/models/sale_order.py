# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
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
                set(res[sale.id])
                | set(group_picking)
                | set(sale.picking_ids.ids)
            )
        return res

    @api.multi
    @api.depends("procurement_group_id")
    def _compute_picking_ids(self):
        picking_dic = self._get_all_picking_ids()
        for sale in self:
            sale.delivery_count = len(picking_dic[sale.id])

    @api.multi
    def action_view_delivery(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        picking_ids = self._get_all_picking_ids()[self.id]
        if len(picking_ids) > 1:
            action["domain"] = [("id", "in", picking_ids)]
        elif picking_ids:
            action["views"] = [
                (self.env.ref("stock.view_picking_form").id, "form")
            ]
            action["res_id"] = picking_ids[0]
        return action

    @api.multi
    def action_cancel(self):
        for sale in self:
            rental_pickings = self.env["stock.picking"].search(
                [("rental_order", "=", sale.id)]
            )
            rental_pickings.action_cancel()
        res = super(SaleOrder, self).action_cancel()

    @api.multi
    def create_and_set_rental_onsite_location_route(self):
        """
            This function create the onsite location for the selected
            partner address and its rental route automatically.
        """
        self.ensure_one()
        # create a intenal location for partner_shipping_id
        if not self.partner_shipping_id:
            raise UserError(_("No found partner address"))
        partner = self.partner_shipping_id
        if not self.warehouse_id.rental_allowed:
            raise UserError(
                _("The selected warehouse is not allowed for rental.")
            )
        if not self.warehouse_id.rental_route_id:
            raise UserError(
                _("No found default Route of the selected warehouse.")
            )
        rental_route = self.warehouse_id.rental_route_id
        if not self.warehouse_id.rental_out_location_id:
            raise UserError(
                _("No found default Route out location of warehouse.")
            )
        rental_out_location = self.warehouse_id.rental_out_location_id
        if not self.warehouse_id.rental_in_location_id:
            raise UserError(
                _("No found default Route in location of warehouse.")
            )
        rental_in_location = self.warehouse_id.rental_in_location_id
        if not self.warehouse_id.int_type_id:
            raise UserError(
                _('No found default picking type "internal" of warehouse.')
            )
        location_name = "Location [%s]" % self.partner_shipping_id.name
        new_location = rental_out_location.copy({"name": location_name})

        # set onsite location of partner address
        self.partner_shipping_id.rental_onsite_location_id = new_location
        self.partner_shipping_id.property_stock_customer = new_location

        # Create a new route for the new location
        route_name = "Rent [%s]" % self.partner_shipping_id.name
        new_route = self.warehouse_id.rental_route_id.copy(
            {"name": route_name}
        )
        new_push_rule = new_route.push_ids[0]
        new_pull_rule = new_route.pull_ids[0]
        for push_rule in new_route.push_ids:
            push_rule.write(
                {
                    "location_from_id": new_location.id,
                    "picking_type_id": self.warehouse_id.int_type_id.id,
                }
            )
        for pull_rule in new_route.pull_ids:
            pull_rule.write(
                {
                    "location_id": new_location.id,
                    "picking_type_id": self.warehouse_id.int_type_id.id,
                }
            )
        self.partner_shipping_id.rental_onsite_location_route = new_route

        # TODO create route for selling from the new location
        # Update shippments and moves and procurements
        for picking in self.picking_ids:
            if (
                picking.location_id.id == rental_in_location.id
                and picking.location_dest_id.id == rental_out_location.id
            ):
                picking.location_dest_id = new_location
                for move in picking.move_lines:
                    # if move.procurement_id:
                    #    move.procurement_id.rule_id = new_pull_rule.id
                    move.write(
                        {
                            "location_dest_id": new_location.id,
                            "rule_id": new_pull_rule.id,
                        }
                    )
            elif (
                picking.location_dest_id.id == rental_in_location.id
                and picking.location_id.id == rental_out_location.id
            ):
                picking.location_id = new_location
                for move in picking.move_lines:
                    move.write(
                        {
                            "location_id": new_location.id,
                            "rule_id": new_pull_rule.id,
                            "push_rule_id": new_push_rule.id,
                        }
                    )
