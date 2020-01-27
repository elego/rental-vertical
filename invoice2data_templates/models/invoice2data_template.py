# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from hashlib import sha256

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import os
from tempfile import mkstemp
import logging


logger = logging.getLogger(__name__)

try:
    from invoice2data.main import extract_data
    from invoice2data.extract.loader import read_templates
    from invoice2data.main import logger as loggeri2data
except ImportError:
    logger.debug("Cannot import invoice2data")


class I2DTemplate(models.Model):
    _name = "invoice2data.template"
    _description = "I2D Template"

    name = fields.Char(string="Name", required=True)
    template = fields.Text(string='Template Content')

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env["res.company"]._company_default_get(
            "account.invoice2data.template"
        )
    )
    active = fields.Boolean(default=True)

    c_hash = fields.Char(string="Template Hash", compute="_compute_hash")

    @api.multi
    @api.depends('template')
    def _compute_hash(self):
        """ Computes the hash of of the template content and use it as file name"""
        local_templates_dir = tools.config.get(
            "invoice2data_templates_dir", False
        )
        logger.debug(
            "invoice2data local_templates_dir=%s", local_templates_dir
        )
        if not(local_templates_dir and os.path.isdir(local_templates_dir)):
            logger.debug(
                "local_templates_dir %s doesn't exist on disk" % local_templates_dir)
        for tmp in self:
            if not self.name:
                continue
            # calculate the hash
            cnt = "%s %s %s" % (tmp.company_id.id, tmp.name, tmp.template)
            hash_string = sha256(cnt.encode('utf-8'))
            # write the template
            with open(os.path.join(local_templates_dir, hash_string), "wb+") as f:
                f.write(self.template)
        return hash_string
