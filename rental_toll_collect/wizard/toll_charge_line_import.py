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
    'advanced': False,
    'date_format': '%d.%m.%Y',
    'datetime_format': '',
    'encoding': 'iso-8859-9',
    'fields': [],
    'float_decimal_separator': '.',
    'float_thousand_separator': ',',
    'headers': True,
    'keep_matches': False,
    'name_create_enabled_fields': {},
    'quoting': '"',
    'separator': ';',
}

IMPORT_MAPPINGS = [
    {'column_name': '6020986205', 'field_name': False, 'id': 1},
    {'column_name': 'kfz-kennz.', 'field_name': 'vehicle_reg_number', 'id': 2},
    {'column_name': 'datum', 'field_name': 'start_date', 'id': 3},
    {'column_name': 'start', 'field_name': 'start_time', 'id': 4},
    {'column_name': 'buchungsnummer', 'field_name': 'booking_number', 'id': 5},
    {'column_name': 'art', 'field_name': 'toll_type', 'id': 6},
    {'column_name': 'auffahrt', 'field_name': 'drive', 'id': 7},
    {'column_name': 'über', 'field_name': 'drive_via', 'id': 8},
    {'column_name': 'abfahrt', 'field_name': 'departure', 'id': 9},
    {'column_name': 'kostenstelle', 'field_name': 'cost_center', 'id': 10},
    {'column_name': 'tarifmodell', 'field_name': 'tariff_model', 'id': 11},
    {'column_name': 'achsklasse', 'field_name': 'axis_class', 'id': 12},
    {'column_name': 'gewichtsklasse', 'field_name': 'weight_class', 'id': 13},
    {'column_name': 'schadstoffklasse', 'field_name': 'polution_class', 'id': 14},
    {'column_name': 'straßenbetreiber', 'field_name': 'road_operator', 'id': 15},
    {'column_name': 'verf.¹', 'field_name': 'procedure', 'id': 16},
    {'column_name': 'km', 'field_name': 'kilometer', 'id': 17},
    {'column_name': 'eur', 'field_name': 'toll_charge', 'id': 18}
]


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
            fields = [m['field_name'] for m in IMPORT_MAPPINGS]
            columns = [m['column_name'] for m in IMPORT_MAPPINGS]
            wizard = self.env['base_import.import'].create({
                'res_model': "toll.charge.line",
                'file_type': 'text/csv',
                'file_name': self.filename,
                'file': base64.b64decode(self.data_file),
            })
            wizard= wizard.with_context(product_id=self.product_id.id)
            res = wizard.do(fields, columns, OPTIONS, dryrun=False)
            return res

