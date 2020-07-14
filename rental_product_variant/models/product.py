# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_product_identification_number = fields.Boolean(
        string="Show Product Identification Number",
        help="If checked, the product identification number "
             "is displayed in product form view.",
    )
    show_vehicle_number = fields.Boolean(
        string="Show Vehicle Identification Number",
        help="If checked, the vehicle identification number "
             "is displayed in product form view.",
    )
    show_license_plate = fields.Boolean(
        string="Show License Plate",
        help="If checked, the license plate is displayed in "
             "product form view.",
    )
    show_init_regist = fields.Boolean(
        string='Show Initial Registration',
        help="If checked, the initial registration is displayed "
             "in product form view.",
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    additional_info = fields.Html(
        string="Additional Information",
        translate=True,
    )
    further_ref = fields.Char(
        string="Further Reference",
    )
    qr_code = fields.Char(
        string="QR-Code",
    )
    manu_year = fields.Char(
        string="Year of Manufacture",
    )
    manu_id = fields.Many2one(
        comodel_name='product.manufacturer',
        string="Manufacturer",
    )
    manu_type_id = fields.Many2one(
        comodel_name='product.manufacturer.type',
        string="Type",
        ondelete='set null',
    )
    fleet_type_id = fields.Many2one(
        comodel_name='fleet.type',
        string="Fleet Type",
        ondelete='set null',
    )

    # Category special fields
    product_identification_number = fields.Char(
        string="Product Identification Number (PIN)",
    )
    vehicle_number = fields.Char(
        string="Vehicle Identification Number (VIN)",
    )
    license_plate = fields.Char(
        string="License Plate",
    )
    init_regist = fields.Date(
        string="Initial Registration",
    )
    show_product_identification_number = fields.Boolean(
        string="Show Product Identification Number",
        related="categ_id.show_product_identification_number",
    )
    show_vehicle_number = fields.Boolean(
        string="Show Vehicle Identification Number",
        related="categ_id.show_vehicle_number",
    )
    show_license_plate = fields.Boolean(
        string="Show License Plate",
        related="categ_id.show_license_plate",
    )
    show_init_regist = fields.Boolean(
        string='Show Initial Registration',
        related="categ_id.show_init_regist",
    )

    # Lists
    rental_order_ids = fields.One2many(
        comodel_name='sale.rental',
        inverse_name='rented_product_id',
        string='Rental Orders',
    )
    stock_move_ids = fields.One2many(
        comodel_name='stock.move',
        inverse_name='product_id',
        string='Stock Moves',
    )

    # Smartbutton Counts
    #TODO Delete field in next Baseline
    invoice_count = fields.Integer('Invoices')

    in_invoice_count = fields.Integer(
        compute='_compute_invoice_count',
        string="In Inv.",
        help="This is the total number of in invoices including "
             "invoice lines with this product.",
    )
    out_invoice_count = fields.Integer(
        compute='_compute_invoice_count',
        string="Out Inv.",
        help="This is the total number of out invoices including "
             "invoice lines with this product.",
    )
    so_count = fields.Integer(
        compute='_compute_so_count',
        string="Sales",
        help="This it the total number of sale orders including "
             "order lines with this product.",
    )
    po_count = fields.Integer(
        compute='_compute_po_count',
        string="Purchase",
        help="This it the total number of purchase orders including "
             "order lines with this product or related analytic account.",
    )
    rental_count = fields.Integer(
        compute="_compute_rental_count",
        string="Rental",
        help="This it the total number of rental orders including "
             "order lines with this product.",
    )

    @api.multi
    def _get_sale_order_ids(self, type_id):
        self.ensure_one()
        sols = self.env['sale.order.line'].search([
            '|',
            ('product_id', '=', self.id),
            ('product_id', 'in', self.rental_service_ids.ids),
        ])
        return list(set([l.order_id.id for l in sols if l.order_id.type_id == type_id]))

    @api.multi
    def _get_purchase_order_ids(self):
        self.ensure_one()
        if self.expense_analytic_account_id:
            domain = ['|', ('product_id', '=', self.id),
                      ('account_analytic_id', '=', self.expense_analytic_account_id.id)]
        else:
            domain = [('product_id', '=', self.id)]
        pols = self.env['purchase.order.line'].search(domain)
        return list(set([l.order_id.id for l in pols]))

    @api.multi
    def _get_invoice_ids(self, inv_types=[]):
        self.ensure_one()
        ails = self.env['account.invoice.line'].search([
            '|',
            ('product_id', '=', self.id),
            ('product_id', 'in', self.rental_service_ids.ids),
        ])
        return list(set([l.invoice_id.id for l in ails if l.invoice_id.type in inv_types]))

    @api.multi
    def action_view_sale_order(self):
        self.ensure_one()
        type_id = self.env.ref('sale_order_type.normal_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        action = self.env.ref('sale.action_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_rental_order(self):
        self.ensure_one()
        type_id = self.env.ref('rental_base.rental_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        action = self.env.ref('rental_base.action_rental_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_all_purchase_order(self):
        self.ensure_one()
        record_ids = self._get_purchase_order_ids()
        tree_view_id = self.env.ref("purchase.purchase_order_tree").id
        form_view_id = self.env.ref("purchase.purchase_order_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Purchase Orders'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'purchase.order',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            'context': "{'search_default_group_by_order_type': 1}"
            }

    @api.multi
    def action_view_invoice(self):
        self.ensure_one()
        inv_type =  self.env.context.get('inv_type')
        record_ids = self._get_invoice_ids(inv_type)
        action = {}
        if inv_type == 'in_invoice':
            action = self.env.ref('account.').read([])[0]
            action['domain'] = [('id','in', record_ids)]
        elif inv_type == 'out_invoice':
            action = self.env.ref('account.action_invoice_tree1').read([])[0]
            action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_all_invoice(self):
        self.ensure_one()
        record_ids = self._get_invoice_ids(inv_types=['in_invoice', 'out_invoice'])
        tree_view_id = self.env.ref("account.invoice_tree").id
        form_view_id = self.env.ref("account.invoice_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Invoices'),
            'target': 'current',
            'view_mode': 'tree,form',
            'view_ids': [tree_view_id, form_view_id],
            'res_model': 'account.invoice',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            'context': "{'search_default_group_by_type': 1}"
            }

    @api.multi
    def _compute_invoice_count(self):
        for rec in self:
            rec.in_invoice_count = len(rec._get_invoice_ids(inv_types=['in_invoice']))
            rec.out_invoice_count = len(rec._get_invoice_ids(inv_types=['out_invoice']))

    @api.multi
    def _compute_so_count(self):
        type_id = self.env.ref('sale_order_type.normal_sale_type')
        for rec in self:
            rec.so_count = len(rec._get_sale_order_ids(type_id))

    @api.multi
    def _compute_rental_count(self):
        type_id = self.env.ref('rental_base.rental_sale_type')
        for rec in self:
            rec.rental_count = len(rec._get_sale_order_ids(type_id))

    @api.multi
    def _compute_po_count(self):
        for rec in self:
            rec.po_count = len(rec._get_purchase_order_ids())


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _description = 'Product Manufacturer'

    name = fields.Char(
        string="Name",
    )
    manufacturer_type_ids = fields.One2many(
        comodel_name='product.manufacturer.type',
        inverse_name='manufacturer_id',
    )


class ProductManufacturerType(models.Model):
    _name = 'product.manufacturer.type'
    _description = 'Product Manufacturer Type'

    name = fields.Char(
        string='Name',
    )
    manufacturer_id = fields.Many2one(
        comodel_name='product.manufacturer',
        string="Manufacturer",
    )


class FleetType(models.Model):
    _name = 'fleet.type'
    _description = 'Fleet Type'

    name = fields.Char(
        string="Name",
        translate=True,
    )
