# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_id = fields.Many2one(
        comodel_name = 'product.product',
        string = 'Product Instance',
        domain = "[('product_instance', '=', True)]",
    )

    tracking = fields.Selection(
        selection = [
            ('serial', 'By Unique Serial Number'),
            ('lot', 'By Lots'),
            ('none', 'No Tracking'),
        ],
        string = 'Tracking',
        related = 'product_id.tracking',
    )

    lot_id = fields.Many2one(
        comodel_name = 'stock.production.lot',
        string = 'Serial Number',
    )

    repair_ids = fields.One2many(
        comodel_name = 'repair.order',
        inverse_name = 'project_task_id',
        string = 'Repair Orders',
    )

    vendor_repair_ids = fields.One2many(
        comodel_name = 'purchase.order',
        inverse_name = 'project_task_id',
        string = 'Vendor Repair Orders',
    )

    phone = fields.Char(
        string = 'Phone',
        help = 'Phone number',
    )

    mobile = fields.Char(
        string = 'Mobile',
        help = 'Mobile number',
    )


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(ProjectTask, self)._onchange_partner_id()
        self.phone = self.partner_id.phone
        self.mobile = self.partner_id.mobile
