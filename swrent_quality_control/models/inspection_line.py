# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class QcInspectionLine(models.Model):
    _inherit = 'qc.inspection.line'

    reason = fields.Text(string="Reason behind failure")