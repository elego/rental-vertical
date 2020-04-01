from odoo import api, exceptions, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    refund_needed = fields.Boolean(
        string='Refund needed',
        copy=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'open': [('readonly', False)],
        },
        track_visibility='onchange',
    )

    clarify_needed = fields.Boolean(
        string='Clarify needed',
        copy=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'open': [('readonly', False)],
        },
        track_visibility='onchange',
    )

    checks_finished = fields.Boolean(
        string='Checks finished',
        copy=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
        track_visibility='onchange',
    )

    payment_release = fields.Boolean(
        string='Release payment',
        copy=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
        track_visibility='onchange',
    )

    forward_invoice_needed = fields.Boolean(
        string='Forward Invoice needed',
        copy=False,
        default=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'open': [('readonly', False)],
        },
        help="If this vendor bill requires to forward this invoice, please activate this checkbox.",
    )

    origin_invoice = fields.Many2one(
        comodel_name='account.invoice',
        ondelete='restrict',
        string='Origin Invoice',
        copy=False,
    )

    has_non_canceled_forward_invoices = fields.Boolean(
        compute='_compute_forward_invoices',
        readonly=True,
    )

    forward_invoice_count = fields.Integer(
        string='Forward Invoice Count',
        compute='_compute_forward_invoices',
        readonly=True,
        copy=False,
    )

    forward_invoice_ids = fields.Many2many(
        "account.invoice",
        string='Invoices',
        compute="_compute_forward_invoices",
        readonly=True,
        copy=False,
    )

    @api.multi
    def invoice_checks(self):
        for order in self:
            if order.invoice_line_ids.filtered(lambda l: not l.account_analytic_id):
                msg = _("No analytic account was set in some lines of the invoice.")
                raise exceptions.UserError(msg)

    @api.multi
    def action_refund_needed(self):
        self.write({
            'refund_needed': True,
        })

    @api.multi
    def action_clarify_needed(self):
        self.invoice_checks()
        self.write({
            'clarify_needed': True,
            'checks_finished': True,
        })

    @api.multi
    def action_clarify_completed(self):
        self.write({
            'clarify_needed': False,
        })

    @api.multi
    def action_checks_finished(self):
        self.invoice_checks()
        self.write({
            'checks_finished': True,
        })

    @api.multi
    def action_payment_release(self):
        self.write({
            'payment_release': True,
        })

    @api.multi
    def _compute_forward_invoices(self):
        for order in self:
            domain = [('origin_invoice', '=', order.id)]
            non_canceled_domain = domain + [('state', '!=', 'cancel')]
            forward_invoice_ids = self.search(domain)
            non_canceled_forward_invoice_ids = self.search(non_canceled_domain)
            order.forward_invoice_ids = forward_invoice_ids
            order.forward_invoice_count = len(forward_invoice_ids)
            order.has_non_canceled_forward_invoices = bool(non_canceled_forward_invoice_ids)

    @api.multi
    def action_view_forward_invoices(self):
        invoices = self.mapped('forward_invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.invoice_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_invoice_open(self):
        self.invoice_checks()
        return super(AccountInvoice, self).action_invoice_open()

