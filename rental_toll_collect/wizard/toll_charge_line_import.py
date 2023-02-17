# Part of rental-vertical See LICENSE file for full copyright and licensing details.
import base64
import logging
import os

from odoo import _, fields, models
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

MIMETYPE_CSV = "text/csv"

OPTIONS = {
    "advanced": False,
    "date_format": "%d.%m.%Y",
    "datetime_format": "",
    "encoding": "iso-8859-9",
    "fields": [],
    "float_decimal_separator": ",",
    "float_thousand_separator": ".",
    "headers": True,
    "keep_matches": False,
    "name_create_enabled_fields": {},
    "quoting": '"',
    "separator": ";",
}

IMPORT_MAPPINGS = [
    {
        "column_name": "6020986205",
        "field_name": False,
        "id": 1,
    },  # TODO: Should this be hardcoded here?
    {"column_name": "kfz-kennz.", "field_name": "license_plate", "id": 2},
    {"column_name": "datum", "field_name": "start_date", "id": 3},
    {"column_name": "start", "field_name": "start_time", "id": 4},
    {"column_name": "buchungsnummer", "field_name": "booking_number", "id": 5},
    {"column_name": "art", "field_name": "toll_type", "id": 6},
    {"column_name": "auffahrt", "field_name": "route_ramp", "id": 7},
    {"column_name": "über", "field_name": "route_via", "id": 8},
    {"column_name": "abfahrt", "field_name": "route_exit", "id": 9},
    {"column_name": "kostenstelle", "field_name": "analytic_account", "id": 10},
    {"column_name": "tarifmodell", "field_name": "tariff_model", "id": 11},
    {"column_name": "achsklasse", "field_name": "axle_class", "id": 12},
    {"column_name": "gewichtsklasse", "field_name": "weight_class", "id": 13},
    {"column_name": "schadstoffklasse", "field_name": "polution_class", "id": 14},
    {"column_name": "straßenbetreiber", "field_name": "road_operator", "id": 15},
    {"column_name": "verf.¹", "field_name": "procedure", "id": 16},
    {"column_name": "km", "field_name": "distance", "id": 17},
    {"column_name": "eur", "field_name": "amount", "id": 18},
]


class TollChargeLineBaseImport(models.TransientModel):
    _inherit = "base_import.import"

    def parse_preview(self, options, **kwargs):
        self.ensure_one()
        if self.res_model == "toll.charge.line":
            options.update(OPTIONS)
        wizard = super(TollChargeLineBaseImport, self)
        res = wizard.parse_preview(options, **kwargs)
        return res


class TollChargeLineImport(models.TransientModel):
    _name = "toll.charge.line.import"
    _description = "Wizard for importing csv-file containing toll collect data"

    data_file = fields.Binary(
        string="File",
        required=True,
    )
    filename = fields.Char(
        string="Filename",
    )

    def _check_csv(self, data_file, filename):
        return (
            filename
            and os.path.splitext(filename)[1] == ".csv"
            or guess_mimetype(data_file) == MIMETYPE_CSV
        )

    def import_toll_charge_lines(self):
        self.ensure_one()
        if self._check_csv(self.data_file, self.filename):
            fields = [m["field_name"] for m in IMPORT_MAPPINGS]
            columns = [m["column_name"] for m in IMPORT_MAPPINGS]
            wizard = self.env["base_import.import"].create(
                {
                    "res_model": "toll.charge.line",
                    "file_type": "text/csv",
                    "file_name": self.filename,
                    "file": base64.b64decode(self.data_file),
                }
            )
            res = wizard.do(fields, columns, OPTIONS, dryrun=False)
            messages = res.get("messages", [])
            errors = list(filter(lambda m: m["type"] == "error", messages))
            if errors:
                aoid = "rental_toll_collect.toll_charge_line_action"
                self.env.ref(aoid).id
                _("Try again with Import button to see details")
                err_fmt = _(
                    "%s Errors were found during the import! "
                    "The first one is: \n\n %s"
                )
                err_msg = err_fmt % (len(errors), errors[0]["message"])
                raise Warning(err_msg)
                # raise RedirectWarning(err_msg , action_id, go_msg)
        action = self.env.ref("rental_toll_collect.toll_charge_line_action")
        return action.read()[0]
