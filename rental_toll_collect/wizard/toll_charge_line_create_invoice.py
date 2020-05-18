from odoo import models, api, fields, _


class TollChargeLineInvoice(models.TransientModel):
    _name = "toll.charge.line.create_invoice"
    _description = "Wizard for creating an invoice from toll charge line(s)."

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string='"Partner',
        help="Please set a customer to invoice the chosen toll charge line(s).",
        domain=[("customer", "=", True)],
        required=True,
    )

    def _create_invoice_template(self, partner):
        # prepare the outgoing invoice
        invoice_context = {
            'type': 'out_invoice',
            'journal_type': 'sale',
        }
        invoice = self.env['account.invoice'].with_context(invoice_context).create({
            'partner_id': partner.id,
        })
        invoice._onchange_partner_id_account_invoice_pricelist()
        invoice._onchange_journal_id()
        return invoice

    @api.multi
    def create_invoice(self):
        self.ensure_one()
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        toll_line_ids = self.env['toll.charge.line'].browse(active_ids).filtered(
            lambda l: l.chargeable and not l.invoiced
        )
        invoice = self._create_invoice_template(self.partner_id)
        values = invoice.get_toll_charge_invoice_line_values(toll_line_ids)
        invoice.create_toll_charge_invoice_lines(values)

        for tcl in toll_line_ids:
            tcl.write({'invoice_id': invoice.id, })
        return invoice

    @api.multi
    def action_view_invoice(self):
        self.ensure_one()
        record_id = self.create_invoice()
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'res_id': record_id.id,
        }
