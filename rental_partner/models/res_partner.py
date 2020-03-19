# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PartnerTitle(models.Model):
    _name = 'res.partner.degree'
    _order = 'name'
    _description = 'Partner Degree'

    name = fields.Char(string='Degree Name', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    degree = fields.Many2one('res.partner.degree', string='Degree')
    type = fields.Selection(selection_add=[('branch', 'Branch')])

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            lang_list = self.env['res.lang'].get_installed()
            country_code = self.country_id.code
            if country_code.upper() == 'DE' and 'de_DE' in dict(lang_list):
                self.lang = 'de_DE'
        return super(ResPartner, self)._onchange_country_id()

    def _get_contact_name(self, partner, name):
        if partner.parent_id.type == 'branch':
            return "%s, %s" % (partner.parent_id.display_name, name)
        else:
            return "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
