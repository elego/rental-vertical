# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class FSMEquipment(models.Model):
    _inherit = 'fsm.equipment'

    owned_by_id = fields.Many2one('res.partner', string='Owned By')
    history_file_id = fields.Many2one('fsm.equipment.history.file', string='History File')

    description = fields.Char('Description') # Bezeichnung
    internal_ref = fields.Char('Internal Reference') # Kurzbezeichnung/Interne Referenz
    other_ref = fields.Char('Other Reference') # Weitere Referenzen
    barcode = fields.Char('Barcode') # Stichcode
    qr_code = fields.Char('QR-Code')
    manu_year = fields.Char('Year of Manufacture')
    category_id = fields.Many2one('fsm.equipment.category', 'Category')
    brand = fields.Many2one('product.brand', ' Brand') #Marke
    brand_type = fields.Many2one('product.brand.type', 'Branch Type') #Marke Typ
    fleet_type = fields.Many2one('fleet.type', 'Fleet Type') #Flottentyp
    equipment_time_line_ids = fields.One2many('fsm.equipment.time.line', 'equipment_id', 'Time Lines')

    @api.model
    def create(self, vals):
        res = super(FSMEquipment, self).create(vals)
        if vals.get('history_file_id', False):
            res.history_file_id.equipment_id = res.id
        return res

    @api.multi
    def write(self, vals):
        for equipment in self:
            prev_history_file = equipment.history_file_id
            res = super(FSMEquipment, equipment).write(vals)
            if 'history_file_id' in vals:
                if prev_history_file:
                    prev_history_file.equipment_id = False
                if equipment.history_file_id:
                    equipment.history_file_id.equipment_id = equipment.id
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    history_file_relevant = fields.Boolean(
        string='History File relevant', default=False,
        help='This product is part of a history file.')
    history_file_obligatory = fields.Boolean(
        string='History File obligatory', default=False,
        help='You need to create a history file for this product.')


class FSMEquipmentCategory(models.Model):
    _name = 'fsm.equipment.category'

    name = fields.Char('Name')


class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char('Name')
    brand_type_ids = fields.One2many('product.brand.type', 'brand_id')


class ProductBrandType(models.Model):
    _name = 'product.brand.type'

    name = fields.Char('Name')
    brand_id = fields.Many2one('product.brand', 'Brand')


class FleetType(models.Model):
    _name = 'fleet.type'

    name = fields.Char('Name')

class FSMEquipmentTimeLine(models.Model):
    _name = 'fsm.equipment.time.line'

    equipment_id = fields.Many2one('fsm.equipment', 'Equipment')
    type = fields.Many2one('Type', selection=[
        ('rental', 'Rental'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('delivery', 'Delivery'),
    ])
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')

