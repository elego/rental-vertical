# Copyright 2019 Elego Software Solutions GmbH (http://www.elego.de/)
# @author: Yurdik Cervantes Mendoza <ycervantes@elegosoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import logging
logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='set null')

    type = fields.Selection(selection_add=[
        ('in_invoice', 'Invoice'),
        ('in_refund', 'Refund')
    ])

    file_type = fields.Selection([
        ('binary', 'Unknown'),
        ('pdf', 'PDF'),
        ('pdf-ubl', 'PDF/UBL'),
        ('pdf-factur-x', 'PDF/Factur-X'),
        ('ubl', 'UBL'),
        ('png', 'PNG'),
        ('jpeg', 'JPG')], string='Doc Type', required=True, default='binary',
        help='Type of the document')

    @api.multi
    def import_button(self):
        pass
