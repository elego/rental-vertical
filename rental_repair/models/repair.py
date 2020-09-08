# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class RepairLine(models.Model):
    _inherit = 'repair.line'

    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag',
        string = 'Analytic Tags',
    )

    analytic_cost = fields.Float(
        'Cost',
    )

    date_end = fields.Date(
        "Date Finished",
        related = "repair_id.date_end",
    )


    @api.onchange('repair_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        res = super(RepairLine, self).onchange_product_id()
        if self.product_id:
            self.analytic_cost = self.product_id.standard_price


class RepairFee(models.Model):
    _inherit = 'repair.fee'

    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag',
        string = 'Analytic Tags',
    )

    analytic_cost = fields.Float(
        'Cost',
    )


    @api.onchange('repair_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        res = super(RepairFee, self).onchange_product_id()
        if self.product_id:
            self.analytic_cost = self.product_id.standard_price


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    project_task_id = fields.Many2one(
        'project.task',
        'Ticket',
        ondelete="set null",
    )

    income_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Income Analytic Account',
        company_dependent=True,
    )

    expense_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Expense Analytic Account',
        company_dependent=True,
    )

    client_order_ref = fields.Char(
        string='Customer Reference',
        help="This is the order number or reference from your customer.",
        copy=False,
    )

    date_order = fields.Date(
        string="Quotation / Order Date",
        default=fields.Date.today,
        help="This date is printed on report as quotation / order date."
    )

    date_start = fields.Date(
        string="Planned Date Start",
        default=fields.Date.today,
        help="This date is the planned start date for the repair."
    )

    date_deadline = fields.Date(
        string="Deadline",
        help="This date is the planned end date for the repair."
    )

    date_end = fields.Date(
        string="Date Finished",
        help="This date is the real end date for the repair."
    )

    operations = fields.One2many(
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'under_repair': [('readonly', False)]
        }
    )

    fees_lines = fields.One2many(
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'under_repair': [('readonly', False)]
        }
    )

    invoice_method = fields.Selection(
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'under_repair': [('readonly', False)]
        }
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Contact Person',
        index=True,
        default=lambda self: self.env.user,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(RepairOrder, self).onchange_product_id()
        if self.product_id:
            self.income_analytic_account_id = self.product_id.income_analytic_account_id.id
            self.expense_analytic_account_id = self.product_id.expense_analytic_account_id.id
            if self.product_id.product_instance:
                self.lot_id = self.product_id.instance_serial_number_id

    @api.multi
    def action_invoice_create(self, group=False):
        res = super(RepairOrder, self).action_invoice_create(group=group)
        for repair in self:
            repair.invoice_id.name = repair.client_order_ref
            if repair.income_analytic_account_id:
                analytic_id = repair.income_analytic_account_id.id
                for operation in repair.operations:
                    if operation.invoiced and operation.invoice_line_id:
                        operation.invoice_line_id.account_analytic_id = analytic_id
                    if operation.invoiced and operation.invoice_line_id and operation.analytic_tag_ids:
                        operation.invoice_line_id.analytic_tag_ids = operation.analytic_tag_ids
                for fee in repair.fees_lines:
                    if fee.invoiced and fee.invoice_line_id:
                        fee.invoice_line_id.account_analytic_id = analytic_id
                    if fee.invoiced and fee.invoice_line_id and fee.analytic_tag_ids:
                        fee.invoice_line_id.analytic_tag_ids = fee.analytic_tag_ids
        return res

    @api.multi
    def action_repair_end(self):
        res = super(RepairOrder, self).action_repair_end()
        for repair in self:
            if not repair.date_end:
                repair.date_end = fields.Date.today()
            repair.create_expense_analytic_lines()
        return res

    @api.multi
    def create_expense_analytic_lines(self):
        """ Create expense account analytic lines for operations and fees
        """
        for repair in self:
            for obj_line in repair.operations:
                vals_line = repair._prepare_expense_analytic_line(obj_line)
                self.env['account.analytic.line'].create(vals_line)
            for obj_line in repair.fees_lines:
                vals_line = repair._prepare_expense_analytic_line(obj_line)
                self.env['account.analytic.line'].create(vals_line)

    @api.multi
    def _prepare_expense_analytic_line(self, line):
        """ Prepare the values used to create() an account.analytic.line
            param: line can only be a record of repair.line or repair.fee
        """
        self.ensure_one()
        amount = line.analytic_cost * line.product_uom_qty * (-1)
        return {
            'name': line.name,
            'date': self.date_end,
            'account_id': self.expense_analytic_account_id.id,
            'tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
            'unit_amount': line.product_uom_qty,
            'product_id': line.product_id and line.product_id.id or False,
            'product_uom_id': line.product_uom and line.product_uom.id or False,
            'amount': amount,
            'ref': self.name,
            'user_id': self._uid,
            'company_id': self.expense_analytic_account_id.company_id.id or self.env.user.company_id.id,
        }
