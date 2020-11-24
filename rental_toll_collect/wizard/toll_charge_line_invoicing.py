# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class TollChargeLineInvoicing(models.TransientModel):
    _name = 'toll.charge.line.invoicing'
    _description = "Wizard for invoicing toll charge lines"

    administrative_charge = fields.Boolean(
        string="Administrative Charge",
        help="If activated, an invoice line with the administrative charge product "
             "is added to the invoice when invoicing toll charge lines.",
        default=True,
    )

    administrative_charge_product = fields.Many2one(
        comodel_name="product.product",
        string='Charge Product',
        default=lambda self: self.env.ref('rental_toll_collect.product_administrative_charge'),
        domain=[('type', '=', 'service')],
    )

    automatic_invoicing = fields.Boolean(
        string="Automatic invoicing",
        help="If activated, draft invoices are created automatically "
             "for the selected toll charge lines using the partner "
             "of the associated sale or rental order.\n"
             "The correct order line is found by comparing its start "
             "and end date with the toll charge line's date.",
        default=True,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.administrative_charge = self.partner_id.administrative_charge
            self.administrative_charge_product = self.partner_id.administrative_charge_product

    @api.model
    def _get_toll_charge_lines(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        return self.env['toll.charge.line'].browse(active_ids)

    def _create_invoice_line(self, values):
        invoice_line = self.env['account.invoice.line'].create(values)
        invoice_line._set_taxes()
        invoice_line.write({
            'price_unit': values.get('price_unit', invoice_line.product_id.list_price)
        })
        return invoice_line

    def action_create_invoice(self):
        """
        Create draft customer invoices for the automatically found partners or manually set partner
        with invoice lines for toll charges and administrative charges.
        """
        tcls = self._get_toll_charge_lines()
        if self.automatic_invoicing:
            partners = tcls.filtered(lambda tcl: not tcl.invoiced and tcl.chargeable).\
                mapped('sale_line_id').mapped('order_id').mapped('partner_invoice_id')
        else:
            partners = self.partner_id

        invoices = self.env['account.invoice']
        for partner in partners:
            invoice_values = self._prepare_invoice(partner)
            invoice = self.env['account.invoice'].create(invoice_values)
            partner_tcls = tcls.filtered(lambda tcl: not tcl.invoiced)
            if self.automatic_invoicing:
                partner_tcls = partner_tcls.filtered(
                    lambda tcl: tcl.sale_line_id and tcl.sale_line_id.order_id.partner_invoice_id == partner
                )
            for product in partner_tcls.mapped('product_id'):
                product_tcls = partner_tcls.filtered(lambda tcl: tcl.product_id == product)
                iline_values = self._prepare_toll_product_line(invoice, product, product_tcls.filtered('chargeable'))
                invoice_line = self._create_invoice_line(iline_values)
                # When invoicing toll charge lines automatically from sale order,
                # the invoice line with the rental service is linked as invoice_line_id.
                # But when invoicing toll charge lines with this wizard,
                # the toll charge is linked as invoice_line_id.
                # Also write the invoice_line_id to lines that are not chargeable
                # to show them in smartbutton in invoice.
                product_tcls.write({
                    'invoice_line_id': invoice_line.id,
                })
            if self.automatic_invoicing:
                administrative_charge = partner.administrative_charge
                charge_product = partner.administrative_charge_product
            else:
                administrative_charge = self.administrative_charge
                charge_product = self.administrative_charge_product
            if administrative_charge:
                charge_values = self._prepare_administrative_product_line(invoice, charge_product)
                self._create_invoice_line(charge_values)
            # calculate invoice's tax lines
            invoice._onchange_invoice_line_ids()
            invoices |= invoice

        action = self.env.ref('account.action_invoice_tree1')
        action_dict = action.read()[0]

        if len(invoices) > 1:
            action_dict['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.invoice_form').id, 'form')]
            if 'views' in action_dict:
                action_dict['views'] = form_view + [
                    (state,  view) for state, view in action[
                        'views'] if view != 'form']
            else:
                action_dict['views'] = form_view
            action_dict['res_id'] = invoices.ids[0]
        return action_dict

    def _prepare_invoice(self, partner):
        vinvoice = self.env['account.invoice'].new({'partner_id': partner.id, 'type': 'out_invoice'})
        vinvoice._onchange_partner_id()
        invoice_vals = vinvoice._convert_to_write(vinvoice._cache)
        invoice_vals.update({
            'origin': _('Toll Collect'),
            'company_id': self.env.user.company_id.id,
        })
        return invoice_vals

    def _prepare_toll_product_line(self, invoice, product, chargeable_toll_lines):
        toll_charge_product = self.env.ref('rental_toll_collect.product_toll')
        dates = chargeable_toll_lines.mapped('toll_date')
        uom_km = self.env.ref('uom.product_uom_km')
        distance = sum(chargeable_toll_lines.mapped('distance'))
        total_amount = sum(chargeable_toll_lines.mapped('amount'))
        license_plate = product.license_plate
        account_id = self.env['account.invoice.line'].get_invoice_line_account(
            invoice.type,
            toll_charge_product,
            invoice.fiscal_position_id,
            invoice.company_id
        )
        # create invoice line name in partner language
        partner_lang = invoice.partner_id.lang
        self.env = api.Environment(self.env.cr, self.env.uid, dict(self.env.context, lang=partner_lang))
        name = toll_charge_product.with_context(lang=partner_lang).display_name + \
            _(" for ") + license_plate + _(" Total Distance: ") + str(round(distance, 2)) + " " + uom_km.name

        vals = {
            'product_id': toll_charge_product.id,
            'quantity': 1.0,
            'uom_id': toll_charge_product.uom_id.id,
            'price_unit': round(total_amount, 2),
            'name': name,
            'toll_product_origin_line_id': False,
            'invoice_id': invoice.id,
            'start_date': min(dates) if dates else False,
            'end_date': max(dates) if dates else False,
            'account_id': account_id.id,
            'account_analytic_id': product.income_analytic_account_id and product.income_analytic_account_id.id,
        }
        return vals

    def _prepare_administrative_product_line(self, invoice, product):
        account_id = self.env['account.invoice.line'].get_invoice_line_account(
            invoice.type,
            product,
            invoice.fiscal_position_id,
            invoice.company_id
        )
        vals = {
            'product_id': product.id,
            'quantity': 1.0,
            'uom_id': product.uom_id.id,
            'price_unit': product.list_price,
            'name': product.with_context(lang=invoice.partner_id.lang).display_name,
            'invoice_id': invoice.id,
            'account_id': account_id.id,
            'account_analytic_id': product.income_analytic_account_id and product.income_analytic_account_id.id,
        }
        return vals
