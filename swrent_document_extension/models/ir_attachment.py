# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    partner_id = fields.Many2one('res.partner',
                                 string='Supplier',
                                 ondelete='set null',
                                 domain=[('supplier', '=', True)])
    user_id = fields.Many2one('res.users', string='Owner', ondelete="restrict")

    invoice_type = fields.Selection(
        selection=[
            ('none', ''),
            ('in_invoice', 'Invoice'),
            ('in_refund', 'Refund')],
        string='Invoice Type', default='none')

    confirmed = fields.Boolean("Confirmed")

    @api.multi
    def action_import_invoice(self):
        self.ensure_one()
        if not self.partner_id:
            raise exceptions.UserError(_('You have to select a Supplier'))
        aiio = self.env['account.invoice.import']
        wizard = aiio.create({
            'invoice_file': self.datas,
            'invoice_filename': self.name,
            'partner_id': self.partner_id.id,
            'invoice_type': self.invoice_type,
        })
        wizard.with_context(default_attachment_id=self.id).import_invoice()
        return True

    @api.multi
    def action_create_draft_invoice(self):
        self.ensure_one()
        invo = self.env['account.invoice']
        iaao = self.env['ir.actions.act_window']
        inv = invo.create({
            'partner_id': self.partner_id.id,
            'type': self.invoice_type,
        })
        inv._onchange_partner_id()
        self.action_assign('account.invoice', inv.id)
        action = iaao.for_xml_id('account', 'action_invoice_tree2')
        action.update({
            'view_mode': 'form,tree,calendar,graph',
            'views': False,
            'res_id': inv.id,
            })
        return action

    @api.multi
    def action_confirm(self):
        self.write({
            'confirmed': True,
        })

    @api.multi
    def action_assign(self, res_model, res_id):
        self.write({
            'res_model': res_model,
            'res_id': res_id,
        })
