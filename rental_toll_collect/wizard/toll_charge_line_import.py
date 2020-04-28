# Part of rental-vertical See LICENSE file for full copyright and licensing details.
import os
import logging
import csv
import base64
from io import StringIO

from odoo import api, models, fields
from odoo.tools.mimetypes import guess_mimetype
from odoo.addons.base_import_async.models.base_import_import import (
    OPT_HAS_HEADER, OPT_QUOTING, OPT_SEPARATOR,
    OPT_CHUNK_SIZE, OPT_USE_QUEUE
)

_logger = logging.getLogger(__name__)

MIMETYPE_CSV = 'text/csv'
OPTIONS = {
    OPT_SEPARATOR: ',',
    OPT_QUOTING: '"',
    OPT_HAS_HEADER: True,
    'date_format': '%Y-%m-%d',
}
# options = {
#     'headers': True,
#     'encoding': 'utf-8',
#     'separator': ';',
#     'quoting': '"',
#     'date_format': '%d.%m.%y',
#     'float_thousand_separator': '.',
#     'float_decimal_separator': ','}


class TollChargeLineImport(models.TransientModel):
    _name = 'toll.charge.line.import'

    data_file = fields.Binary(string='Upload File', required=True)
    filename = fields.Char()
    product_id = fields.Many2one('product.product',
        string='Product')

    def _check_csv(self, data_file, filename):
        return filename and os.path.splitext(filename)[1] == '.csv' or \
            guess_mimetype(data_file) == MIMETYPE_CSV

    

    @api.multi
    def import_toll_charge_lines(self):
        self.ensure_one()
        if self._check_csv(self.data_file, self.filename):
            fields = self.get_fields('toll.charge.line')
            # rows = self._read_csv(OPTIONS)
            # headers, matches = self._match_headers(rows, fields, OPTIONS)
            # for row in rows:
            #     print("================row====", row)
            # print("=============rows======", rows, type(rows))
            wizard = self.env['toll.charge.line.import.wizard'].create({
                'res_model': "toll.charge.line",
                'file_type': 'text/csv',
                'file_name': self.filename,
                'file': base64.b64decode(self.data_file),
            })
            wizard.with_context(product_id=self.product_id.id).do(fields, [], OPTIONS)

    # def run_import_with_partner(self, file_name, file_type):
    #     fields = ['date', 'name', 'partner_id', 'balance', 'amount']
    #     wizard = self.env['toll.charge.line.import'].create({
    #         'res_model': "toll.charge.line",
    #         'file_type': 'text/csv',
    #         'file_name': self.filename,
    #         'file': base64.b64decode(self.data_file),
    #     })
    #     wizard.with_context(product_id=self.product_id.id).do(fields, [], OPTIONS)
            # self._read_csv()
        # toll_obj = self.env['toll.charge.line']
        # data_file = base64.b64decode(self.data_file).encode('utf-8')
        # if not isinstance(data_file, str):
        #     data_file = data_file.strip()
        # file = StringIO(data_file)
        # file.seek(0)
        # reader = csv.reader(file)
        # headers = []
        # for row in reader:
        #     print("===========row=======", row)
        #     headers = row
        #     break
        # lines = []
        # for idx, title in enumerate(headers):
        #     lines.append((0, 0, {'sequence': idx, 'name': title}))
        # print("==============lines=======", lines)
        # if lines:
        #     for statement in toll_obj.browse(
        #             self.env.context.get('active_ids')):
        #         statement.map_line_ids = lines

    # def _check_xls(self, data_file, filename):
    #     return filename and os.path.splitext(filename)[1] == '.xls' or \
    #         guess_mimetype(data_file) == MIMETYPE_XLS
            
    # def _check_xlsx(self, data_file, filename):
    #     return filename and os.path.splitext(filename)[1] == '.xlsx' or \
    #         guess_mimetype(data_file) == MIMETYPE_XLSX
    # def _check_ods(self, data_file, filename):
    #     return filename and os.path.splitext(filename)[1] == '.ods' or \
    #         guess_mimetype(data_file) == MIMETYPE_ODS

    # @api.multi
    # def import_toll_charge_lines(self):
    #     print("=========hhhh===========", self.data_file)
    #     if self._check_csv(self.data_file, self.filename):
    #         return self._import_wizard(self.filename, self.data_file, MIMETYPE_CSV)
        
    # @api.model
    # def _import_wizard(self, file_name, file, file_type):
    #     wizard = self.env['toll.charge.line.import'].create({
    #         'res_model': "toll.charge.line",
    #         'file_type': 'text/csv',
    #         'file_name': self.filename,
    #         'file': base64.b64decode(self.data_file),
    #     })
    #     context = dict(self.env.context)
    #     context.update({'wizard_id': wizard.id})
    #     print("=================context========", context)
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'import_toll_charge_lines',
    #         'params': {
    #             'model': "toll.charge.line",
    #             'filename': self.filename,
    #             'context': context,
    #         }
    #     }

    # -*- coding: utf-8 -*-

# import base64

# from odoo import api, fields, models, _
# from odoo.exceptions import UserError
# from odoo.addons.base.models.res_bank import sanitize_account_number

# import logging
# _logger = logging.getLogger(__name__)


# class AccountBankStatementLine(models.Model):
#     _inherit = "account.bank.statement.line"

#     # Ensure transactions can be imported only once (if the import format provides unique transaction ids)
#     unique_import_id = fields.Char(string='Import ID', readonly=True, copy=False)

#     _sql_constraints = [
#         ('unique_import_id', 'unique (unique_import_id)', 'A bank account transactions can be imported only once !')
#     ]


# class AccountBankStatementImport(models.TransientModel):
#     _name = 'account.bank.statement.import'
#     _description = 'Import Bank Statement'

#     data_file = fields.Binary(string='Bank Statement File', required=True, help='Get you bank statements in electronic format from your bank and select them here.')
#     filename = fields.Char()

    # @api.multi
    # def import_file(self):
    #     """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
    #     self.ensure_one()
    #     # Let the appropriate implementation module parse the file and return the required data
    #     # The active_id is passed in context in case an implementation module requires information about the wizard state (see QIF)
    #     currency_code, account_number, stmts_vals = self.with_context(active_id=self.ids[0])._parse_file(base64.b64decode(self.data_file))
    #     # Check raw data
    #     self._check_parsed_data(stmts_vals)
    #     # Try to find the currency and journal in odoo
    #     currency, journal = self._find_additional_data(currency_code, account_number)
    #     # If no journal found, ask the user about creating one
    #     if not journal:
    #         # The active_id is passed in context so the wizard can call import_file again once the journal is created
    #         return self.with_context(active_id=self.ids[0])._journal_creation_wizard(currency, account_number)
    #     if not journal.default_debit_account_id or not journal.default_credit_account_id:
    #         raise UserError(_('You have to set a Default Debit Account and a Default Credit Account for the journal: %s') % (journal.name,))
    #     # Prepare statement data to be used for bank statements creation
    #     stmts_vals = self._complete_stmts_vals(stmts_vals, journal, account_number)
    #     # Create the bank statements
    #     statement_ids, notifications = self._create_bank_statements(stmts_vals)
    #     # Now that the import worked out, set it as the bank_statements_source of the journal
    #     if journal.bank_statements_source != 'file_import':
    #         # Use sudo() because only 'account.group_account_manager'
    #         # has write access on 'account.journal', but 'account.group_account_user'
    #         # must be able to import bank statement files
    #         journal.sudo().bank_statements_source = 'file_import'
    #     # Finally dispatch to reconciliation interface
    #     action = self.env.ref('account.action_bank_reconcile_bank_statements')
    #     return {
    #         'name': action.name,
    #         'tag': action.tag,
    #         'context': {
    #             'statement_ids': statement_ids,
    #             'notifications': notifications
    #         },
    #         'type': 'ir.actions.client',
    #     }

    # def _journal_creation_wizard(self, currency, account_number):
    #     """ Calls a wizard that allows the user to carry on with journal creation """
    #     return {
    #         'name': _('Journal Creation'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.bank.statement.import.journal.creation',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {
    #             'statement_import_transient_id': self.env.context['active_id'],
    #             'default_bank_acc_number': account_number,
    #             'default_name': _('Bank') + ' ' + account_number,
    #             'default_currency_id': currency and currency.id or False,
    #             'default_type': 'bank',
    #         }
    #     }

    # def _parse_file(self, data_file):
    #     """ Each module adding a file support must extends this method. It processes the file if it can, returns super otherwise, resulting in a chain of responsability.
    #         This method parses the given file and returns the data required by the bank statement import process, as specified below.
    #         rtype: triplet (if a value can't be retrieved, use None)
    #             - currency code: string (e.g: 'EUR')
    #                 The ISO 4217 currency code, case insensitive
    #             - account number: string (e.g: 'BE1234567890')
    #                 The number of the bank account which the statement belongs to
    #             - bank statements data: list of dict containing (optional items marked by o) :
    #                 - 'name': string (e.g: '000000123')
    #                 - 'date': date (e.g: 2013-06-26)
    #                 -o 'balance_start': float (e.g: 8368.56)
    #                 -o 'balance_end_real': float (e.g: 8888.88)
    #                 - 'transactions': list of dict containing :
    #                     - 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
    #                     - 'date': date
    #                     - 'amount': float
    #                     - 'unique_import_id': string
    #                     -o 'account_number': string
    #                         Will be used to find/create the res.partner.bank in odoo
    #                     -o 'note': string
    #                     -o 'partner_name': string
    #                     -o 'ref': string
    #     """
    #     raise UserError(_('Could not make sense of the given file.\nDid you install the module to support this type of file ?'))

    # def _check_parsed_data(self, stmts_vals):
    #     """ Basic and structural verifications """
    #     if len(stmts_vals) == 0:
    #         raise UserError(_('This file doesn\'t contain any statement.'))

    #     no_st_line = True
    #     for vals in stmts_vals:
    #         if vals['transactions'] and len(vals['transactions']) > 0:
    #             no_st_line = False
    #             break
    #     if no_st_line:
    #         raise UserError(_('This file doesn\'t contain any transaction.'))

    # def _check_journal_bank_account(self, journal, account_number):
    #     return journal.bank_account_id.sanitized_acc_number == account_number

    # def _find_additional_data(self, currency_code, account_number):
    #     """ Look for a res.currency and account.journal using values extracted from the
    #         statement and make sure it's consistent.
    #     """
    #     company_currency = self.env.user.company_id.currency_id
    #     journal_obj = self.env['account.journal']
    #     currency = None
    #     sanitized_account_number = sanitize_account_number(account_number)

    #     if currency_code:
    #         currency = self.env['res.currency'].search([('name', '=ilike', currency_code)], limit=1)
    #         if not currency:
    #             raise UserError(_("No currency found matching '%s'.") % currency_code)
    #         if currency == company_currency:
    #             currency = False

    #     journal = journal_obj.browse(self.env.context.get('journal_id', []))
    #     if account_number:
    #         # No bank account on the journal : create one from the account number of the statement
    #         if journal and not journal.bank_account_id:
    #             journal.set_bank_account(account_number)
    #         # No journal passed to the wizard : try to find one using the account number of the statement
    #         elif not journal:
    #             journal = journal_obj.search([('bank_account_id.sanitized_acc_number', '=', sanitized_account_number)])
    #         # Already a bank account on the journal : check it's the same as on the statement
    #         else:
    #             if not self._check_journal_bank_account(journal, sanitized_account_number):
    #                 raise UserError(_('The account of this statement (%s) is not the same as the journal (%s).') % (account_number, journal.bank_account_id.acc_number))

    #     # If importing into an existing journal, its currency must be the same as the bank statement
    #     if journal:
    #         journal_currency = journal.currency_id
    #         if currency is None:
    #             currency = journal_currency
    #         if currency and currency != journal_currency:
    #             statement_cur_code = not currency and company_currency.name or currency.name
    #             journal_cur_code = not journal_currency and company_currency.name or journal_currency.name
    #             raise UserError(_('The currency of the bank statement (%s) is not the same as the currency of the journal (%s).') % (statement_cur_code, journal_cur_code))

    #     # If we couldn't find / can't create a journal, everything is lost
    #     if not journal and not account_number:
    #         raise UserError(_('Cannot find in which journal import this statement. Please manually select a journal.'))

    #     return currency, journal

    # def _complete_stmts_vals(self, stmts_vals, journal, account_number):
    #     for st_vals in stmts_vals:
    #         st_vals['journal_id'] = journal.id
    #         if not st_vals.get('reference'):
    #             st_vals['reference'] = self.filename
    #         if st_vals.get('number'):
    #             #build the full name like BNK/2016/00135 by just giving the number '135'
    #             st_vals['name'] = journal.sequence_id.with_context(ir_sequence_date=st_vals.get('date')).get_next_char(st_vals['number'])
    #             del(st_vals['number'])
    #         for line_vals in st_vals['transactions']:
    #             unique_import_id = line_vals.get('unique_import_id')
    #             if unique_import_id:
    #                 sanitized_account_number = sanitize_account_number(account_number)
    #                 line_vals['unique_import_id'] = (sanitized_account_number and sanitized_account_number + '-' or '') + str(journal.id) + '-' + unique_import_id

    #             if not line_vals.get('bank_account_id'):
    #                 # Find the partner and his bank account or create the bank account. The partner selected during the
    #                 # reconciliation process will be linked to the bank when the statement is closed.
    #                 identifying_string = line_vals.get('account_number')
    #                 if identifying_string:
    #                     partner_bank = self.env['res.partner.bank'].search([('acc_number', '=', identifying_string)], limit=1)
    #                     if partner_bank:
    #                         line_vals['bank_account_id'] = partner_bank.id
    #                         line_vals['partner_id'] = partner_bank.partner_id.id
    #     return stmts_vals

    # def _create_bank_statements(self, stmts_vals):
    #     """ Create new bank statements from imported values, filtering out already imported transactions, and returns data used by the reconciliation widget """
    #     BankStatement = self.env['account.bank.statement']
    #     BankStatementLine = self.env['account.bank.statement.line']

    #     # Filter out already imported transactions and create statements
    #     statement_ids = []
    #     ignored_statement_lines_import_ids = []
    #     for st_vals in stmts_vals:
    #         filtered_st_lines = []
    #         for line_vals in st_vals['transactions']:
    #             if 'unique_import_id' not in line_vals \
    #                or not line_vals['unique_import_id'] \
    #                or not bool(BankStatementLine.sudo().search([('unique_import_id', '=', line_vals['unique_import_id'])], limit=1)):
    #                 filtered_st_lines.append(line_vals)
    #             else:
    #                 ignored_statement_lines_import_ids.append(line_vals['unique_import_id'])
    #                 if 'balance_start' in st_vals:
    #                     st_vals['balance_start'] += float(line_vals['amount'])

    #         if len(filtered_st_lines) > 0:
    #             # Remove values that won't be used to create records
    #             st_vals.pop('transactions', None)
    #             # Create the statement
    #             st_vals['line_ids'] = [[0, False, line] for line in filtered_st_lines]
    #             statement_ids.append(BankStatement.create(st_vals).id)
    #     if len(statement_ids) == 0:
    #         raise UserError(_('You already have imported that file.'))

    #     # Prepare import feedback
    #     notifications = []
    #     num_ignored = len(ignored_statement_lines_import_ids)
    #     if num_ignored > 0:
    #         notifications += [{
    #             'type': 'warning',
    #             'message': _("%d transactions had already been imported and were ignored.") % num_ignored if num_ignored > 1 else _("1 transaction had already been imported and was ignored."),
    #             'details': {
    #                 'name': _('Already imported items'),
    #                 'model': 'account.bank.statement.line',
    #                 'ids': BankStatementLine.search([('unique_import_id', 'in', ignored_statement_lines_import_ids)]).ids
    #             }
    #         }]
    #     return statement_ids, notifications

