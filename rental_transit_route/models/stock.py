# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(
            product_id=product_id, product_qty=product_qty, product_uom=product_uom,
            location_id=location_id, name=name, origin=origin, values=values, group_id=group_id)
        if values.get('planned_in_location_id', False):
            res['location_id'] = values.get('planned_in_location_id')
        return res

    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        """Inherit to write the date of the rental on move"""
        # get value of 3rd. move
        res = super(StockRule, self)._push_prepare_move_copy_values(
            move_to_copy, new_date)
        location_id = res.get('location_id', False)
        # get value of 2nd. stock.move
        if location_id and\
            location_id ==\
            move_to_copy.warehouse_id.transit_out_location_id.id and\
                move_to_copy.sale_line_id and\
                move_to_copy.sale_line_id.rental_type == 'new_rental':
            rental_start_date = move_to_copy.sale_line_id.start_date
            res['date_expected'] = fields.Datetime.to_datetime(rental_start_date)
        # get value of 4th stock.move
        if location_id and\
            location_id ==\
            move_to_copy.warehouse_id.transit_in_location_id.id and\
                move_to_copy.sale_line_id and\
                move_to_copy.sale_line_id.rental_type == 'new_rental':
            rental_end_date = move_to_copy.sale_line_id.end_date + timedelta(days=move_to_copy.sale_line_id.customer_lead)
            res['date_expected'] = fields.Datetime.to_datetime(rental_end_date)

        return res

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

#    rental_view_location_id = fields.Many2one(
#        'stock.location', 'Parent Rental', domain=[('usage', '=', 'view')])
#    rental_in_location_id = fields.Many2one(
#        'stock.location', 'Rental In', domain=[('usage', '=', 'internal')])
#    rental_out_location_id = fields.Many2one(
#        'stock.location', 'Rental Out', domain=[('usage', '!=', 'view')])
#    rental_allowed = fields.Boolean('Rental Allowed')
#    rental_route_id = fields.Many2one(
#        'stock.location.route', string='Rental Route')
#    sell_rented_product_route_id = fields.Many2one(
#        'stock.location.route', string='Sell Rented Product Route')
    rental_transit_route_id = fields.Many2one(
        'stock.location.route', string='Rental Transit Route')
    transit_in_location_id = fields.Many2one(
        'stock.location', 'Transit In', domain=[('usage', '=', 'internal')])
    transit_out_location_id = fields.Many2one(
        'stock.location', 'Transit Out', domain=[('usage', '=', 'internal')])

    @api.onchange('rental_allowed')
    def _onchange_rental_allowed(self):
        res = super(StockWarehouse, self)._onchange_rental_allowed()
        if not self.rental_allowed:
            self.transit_in_location_id = False
            self.transit_out_location_id = False
            self.rental_transit_route_id = False

    def reset_rental_location_and_push_pull_rules(self):
        self.ensure_one()
        self._create_rental_locations()
        rules_to_delete = self.env['stock.rule'].search(
            [
                ('route_id', 'in', (
                    self.rental_route_id.id,
                    self.rental_transit_route_id.id,
                    self.sell_rented_product_route_id.id))])
        rules_to_delete.unlink()
        for rule_vals in self._get_rental_push_pull_rules():
            self.env['stock.rule'].create(rule_vals)
        for rule_vals in self._get_rental_transit_push_pull_rules():
            self.env['stock.rule'].create(rule_vals)

    def _get_rental_transit_push_pull_rules(self):
        self.ensure_one()
        route_obj = self.env['stock.location.route']
        try:
            rental_route = self.env.ref('rental_transit_route.route_warehouse0_rental_transit')
        except Exception:
            rental_routes = route_obj.search([('name', '=', _('Rent Transit'))])
            rental_route = rental_routes and rental_routes[0] or False
        if not rental_route:
            raise UserError(_("Can't find any generic 'Rent Transit' route."))
        if not self.rental_in_location_id:
            raise UserError(_(
                "The Rental Input stock location is not set on the "
                "warehouse %s") % self.name)
        if not self.rental_out_location_id:
            raise UserError(_(
                "The Rental Output stock location is not set on the "
                "warehouse %s") % self.name)
        if not self.transit_in_location_id:
            raise UserError(_(
                "The Transit In stock location is not set on the "
                "warehouse %s") % self.name)
        if not self.transit_out_location_id:
            raise UserError(_(
                "The Transit Out stock location is not set on the "
                "warehouse %s") % self.name)
        rental_pull_rule = {
            'name': self._format_rulename(
                self.rental_in_location_id,
                self.transit_out_location_id, ''),
            'location_src_id': self.rental_in_location_id.id,
            'location_id': self.transit_out_location_id.id,
            'route_id': rental_route.id,
            'action': 'pull',
            'picking_type_id': self.out_type_id.id,
            'warehouse_id': self.id,
        }
        rental_push_rule_1 = {
            'name': self._format_rulename(
                self.transit_out_location_id,
                self.rental_out_location_id, ''),
            'location_src_id': self.transit_out_location_id.id,
            'location_id': self.rental_out_location_id.id,
            'route_id': rental_route.id,
            'action': 'push',
            'picking_type_id': self.int_type_id.id,
            'warehouse_id': self.id,
        }
        rental_push_rule_2 = {
            'name': self._format_rulename(
                self.rental_out_location_id,
                self.transit_in_location_id, ''),
            'location_src_id': self.rental_out_location_id.id,
            'location_id': self.transit_in_location_id.id,
            'route_id': rental_route.id,
            'action': 'push',
            'picking_type_id': self.int_type_id.id,
            'warehouse_id': self.id,
        }
        rental_push_rule_3 = {
            'name': self._format_rulename(
                self.transit_in_location_id,
                self.rental_in_location_id, ''),
            'location_src_id': self.transit_in_location_id.id,
            'location_id': self.rental_in_location_id.id,
            'route_id': rental_route.id,
            'action': 'push',
            'picking_type_id': self.in_type_id.id,
            'warehouse_id': self.id,
        }
        res = [
            rental_pull_rule,
            rental_push_rule_1,
            rental_push_rule_2,
            rental_push_rule_3,
            ]
        return res

    def _create_rental_locations(self):
        res = super(StockWarehouse, self)._create_rental_locations()
        slo = self.env['stock.location']
        for wh in self:
            # create stock locations
            if not wh.transit_in_location_id:
                in_loc = slo.with_context(lang='en_US').search([
                    ('name', 'ilike', 'Transit In'),
                    ('location_id', '=', wh.rental_view_location_id.id),
                    ], limit=1)
                if not in_loc:
                    in_loc = slo.with_context(lang='en_US').create({
                        'name': 'Transit In',
                        'location_id': wh.rental_view_location_id.id,
                        })
                    slo.browse(in_loc.id).name = _('Transit In')
                    logger.debug(
                        'New in transit stock location created ID %d',
                        in_loc.id)
                wh.transit_in_location_id = in_loc.id
            if not wh.transit_out_location_id:
                out_loc = slo.with_context(lang='en_US').search([
                    ('name', 'ilike', 'Transit Out'),
                    ('location_id', '=', wh.rental_view_location_id.id),
                    ], limit=1)
                if not out_loc:
                    out_loc = slo.with_context(lang='en_US').create({
                        'name': 'Transit Out',
                        'location_id': wh.rental_view_location_id.id,
                        })
                    slo.browse(out_loc.id).name = _('Transit Out')
                    logger.debug(
                        'New out Transit stock location created ID %d',
                        out_loc.id)
                wh.transit_out_location_id = out_loc.id

    def write(self, vals):
        if 'rental_allowed' in vals:
            rental_transit_route = self.env.ref(
                'rental_transit_route.route_warehouse0_rental_transit')
            if vals.get('rental_allowed'):
                self._create_rental_locations()
                self.write({
                    'route_ids': [(4, rental_transit_route.id)],
                    'rental_transit_route_id': rental_transit_route.id,
                    })
                for rule_vals in self._get_rental_transit_push_pull_rules():
                    self.env['stock.rule'].create(rule_vals)
            else:
                for wh in self:
                    rules_to_delete = self.env['stock.rule'].search(
                        [('route_id', '=', wh.rental_transit_route_id.id)])
                    rules_to_delete.unlink()
                    wh.write({
                        'route_ids': [(3, rental_transit_route.id)],
                        'rental_transit_route_id': False,
                    })
        return super(StockWarehouse, self).write(vals)

#TODO Set Date
#class StockRule(models.Model):
#    _inherit = 'stock.rule'
#
#    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
#        """Inherit to write the end date of the rental on the return move"""
#        res = super(StockRule, self)._push_prepare_move_copy_values(
#            move_to_copy, new_date)
#        location_id = res.get('location_id', False)
#        if location_id and\
#            location_id ==\
#            move_to_copy.warehouse_id.rental_out_location_id.id and\
#                move_to_copy.sale_line_id and\
#                move_to_copy.sale_line_id.rental_type == 'new_rental':
#            rental_end_date = move_to_copy.sale_line_id.end_date
#            res['date_expected'] = fields.Datetime.to_datetime(rental_end_date)
#        return res

#TODO Check if it is need for other unit test
#class StockInventory(models.Model):
#    _inherit = 'stock.inventory'
#
#    def create_demo_and_validate(self):
#        silo = self.env['stock.inventory.line']
#        demo_inv = self.env.ref('sale_rental.rental_inventory')
#        rental_in_loc = self.env.ref('stock.warehouse0').rental_in_location_id
#        demo_inv.location_id = rental_in_loc
#        demo_inv.action_start()
#        products = [
#            ('product.consu_delivery_01', 56),
#            ('product.product_product_20', 46),
#            ('product.product_product_25', 2),
#        ]
#        for (product_xmlid, qty) in products:
#            product = self.env.ref(product_xmlid)
#            silo.create({
#                'product_id': product.id,
#                'product_uom_id': product.uom_id.id,
#                'inventory_id': demo_inv.id,
#                'product_qty': qty,
#                'location_id': rental_in_loc.id,
#            })
#        demo_inv.action_validate()
#        return True
