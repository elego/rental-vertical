# -*- coding: utf-8 -*-
# copyrights 2019 SW.Rent All Rights Reserved

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_id = fields.Many2one('fsm.equipment.category', 'Category')
    brand = fields.Many2one('product.brand', ' Brand') #Marke
    brand_type = fields.Many2one('product.brand.type', 'Branch Type') #Marke Typ
    fleet_type = fields.Many2one('fleet.type', 'Fleet Type') #Flottentyp


class FSMEquipmentCategory(models.Model):
    _name = 'fsm.equipment.category'
    _description = 'FSM Equipment Category'

    name = fields.Char('Name')


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char('Name')
    brand_type_ids = fields.One2many('product.brand.type', 'brand_id')


class ProductBrandType(models.Model):
    _name = 'product.brand.type'
    _description = 'Product Brand Type'

    name = fields.Char('Name')
    brand_id = fields.Many2one('product.brand', 'Brand')


class FleetType(models.Model):
    _name = 'fleet.type'
    _description = 'Fleet Type'

    name = fields.Char('Name')
