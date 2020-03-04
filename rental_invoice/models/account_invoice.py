from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    factually_correct = fields.Selection(
        string='Factually correct',
        selection=[
            ('no', 'No'),
            ('yes', 'Yes'),
        ],
        copy=False,
        track_visibility='onchange',
        help="If you expect the supplier to invoice these positions to you, please set this field to 'yes'.",
    )

    arithmetically_correct = fields.Selection(
        string='Arithmetically correct',
        selection=[
            ('no', 'No'),
            ('yes', 'Yes'),
        ],
        copy=False,
        track_visibility='onchange',
        help="If the vendor bill and its positions have the correct quantity, price, taxes, etc., please set this field to 'yes'.",
    )

    customer_invoice_needed = fields.Boolean(
        string='Customer Invoice needed',
        copy=False,
        default=False,
        help="If this vendor bill requires to be invoiced to a customer, please activate this checkbox.",
    )

    origin_invoice = fields.Many2one(
        comodel_name='account.invoice',
        ondelete='restrict',
        string='Origin Invoice',
        copy=False,
    )

    has_non_canceled_customer_invoices = fields.Boolean(
        compute='_compute_customer_invoices',
        readonly=True,
    )

    customer_invoice_count = fields.Integer(
        string='Customer Invoice Count',
        compute='_compute_customer_invoices',
        readonly=True,
        copy=False,
    )

    customer_invoice_ids = fields.Many2many(
        "account.invoice",
        string='Invoices',
        compute="_compute_customer_invoices",
        readonly=True,
        copy=False,
    )

    @api.multi
    def action_set_factual_check_succeeded(self):
        for order in self:
            order.factually_correct = 'yes'
    @api.multi
    def action_set_factual_check_failed(self):
        for order in self:
            order.factually_correct = 'no'

    @api.multi
    def action_set_arithmetical_check_succeeded(self):
        for order in self:
            order.arithmetically_correct = 'yes'
    @api.multi
    def action_set_arithmetical_check_failed(self):
        for order in self:
            order.arithmetically_correct = 'no'

    @api.multi
    def _compute_customer_invoices(self):
        for order in self:
            domain = [('origin_invoice', '=', order.id)]
            non_canceled_domain = domain + [('state', '!=', 'cancel')]
            customer_invoice_ids = self.search(domain)
            non_canceled_customer_invoice_ids = self.search(non_canceled_domain)
            order.customer_invoice_ids = customer_invoice_ids
            order.customer_invoice_count = len(customer_invoice_ids)
            order.has_non_canceled_customer_invoices = bool(non_canceled_customer_invoice_ids)

    @api.multi
    def action_view_customer_invoices(self):
        invoices = self.mapped('customer_invoice_ids')
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
