# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
import operator

from odoo import api, models
from odoo.tools import pycompat
from odoo.tools.translate import _


class Import(models.TransientModel):

    _inherit = "base_import.import"

    @api.model
    def _convert_import_data(self, fields, options):
        # toll.charge .line import : remove rows who has only column
        # same as base method code, additional one line only to filter rows
        if self.res_model == "toll.charge.line":
            # Get indices for non-empty fields
            indices = [index for index, field in enumerate(fields) if field]
            if not indices:
                raise ValueError(_("You must configure at least one field to import"))
            # If only one index, itemgetter will return an atom rather
            # than a 1-tuple
            if len(indices) == 1:
                def mapper(row):
                    return [row[indices[0]]]
            else:
                mapper = operator.itemgetter(*indices)
            # Get only list of actually imported fields
            import_fields = [f for f in fields if f]

            _file_length, rows_to_import = self._read_file(options)
            # fileter rows here
            rows_to_import = itertools.filterfalse(
                lambda row: len(row) < 2, rows_to_import
            )
            if options.get("headers"):
                rows_to_import = itertools.islice(rows_to_import, 1, None)
            data = [
                list(row) for row in map(mapper, rows_to_import)
                # don't try inserting completely empty rows (e.g. from
                # filtering out o2m fields)
                if any(row)
            ]

            return data, import_fields
        else:
            return super(Import, self)._convert_import_data(fields, options)
