from odoo import api, fields, models, exceptions, _


class CreateCustomerInvoice(models.TransientModel):
    _name = 'account.invoice.create_customer_invoice'
    _description = 'Wizard for creating customer invoices from vendor invoices'

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        domain=[('customer', '=', True)],
        required=True,
    )

    @api.multi
    def create_customer_invoice(self):
        for invoice_vendor in self.env['account.invoice'].browse(self.env.context['active_ids']):
            used_products = set(l.product_id for l in invoice_vendor.invoice_line_ids if l.product_id)
            sale_products = set(p for p in used_products if p.sale_ok)
            non_sale_products = used_products - sale_products
            if non_sale_products:
                msg = _("""
                The customer invoice cannot be created because the following products are not sellable:
                {}

                Please set the products flag \"can be sold\" to true, if you really want to invoice these products to the customer.
                """)
                msg_products = "\n".join(["- %s" % _(p.display_name) for p in non_sale_products])
                raise exceptions.ValidationError(msg.format(msg_products))

            invoice_customer_context = {
                'type':'out_invoice',
                'journal_type': 'sale',
            }
            invoice_customer_obj =  self.env['account.invoice'].with_context(invoice_customer_context)
            invoice_customer = invoice_customer_obj.create({
                'partner_id': self.partner_id.id,
                'origin_invoice': invoice_vendor.id,
            })
            invoice_customer._onchange_partner_id_account_invoice_pricelist()
            invoice_customer._onchange_journal_id()

            invoice_customer_line_context = {
                'type': invoice_customer.type,
                'journal_id': invoice_customer.journal_id.id,
                'default_invoice_id': invoice_customer.id,
            }
            invoice_customer_line_obj =  self.env['account.invoice.line'].with_context(invoice_customer_line_context)
            for v_line in invoice_vendor.invoice_line_ids:
                c_line = invoice_customer_line_obj.create({
                    'product_id': v_line.product_id.id,
                    'quantity': v_line.quantity,
                    'uom_id': v_line.uom_id.id,
                    'discount': v_line.discount,
                    'price_unit': v_line.price_unit,
                    'name': v_line.name,
                    'start_date': v_line.start_date,
                    'end_date': v_line.end_date,
                })
                c_line._onchange_product_id()
                c_line._onchange_uom_id()
                c_line._onchange_account_id()
                c_line.price_unit = v_line.price_unit
                if not c_line.account_analytic_id and v_line.account_analytic_id:
                    c_line.account_analytic_id = v_line.account_analytic_id

            invoice_customer._onchange_cash_rounding()
            invoice_customer._onchange_invoice_line_ids()
