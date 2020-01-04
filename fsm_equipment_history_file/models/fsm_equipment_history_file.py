# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class FSMEquipmentHistoryFile(models.Model):
    _name = 'fsm.equipment.history.file'
    _description = 'Equipment history file'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', size=64)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product', ondelete='restrict', index=True,
        domain=[('history_file_obligatory', '=', True)])
    equipment_id = fields.Many2one(
        comodel_name='fsm.equipment',
        string='Equipment', ondelete='restrict', index=True)
    lot_id = fields.Many2one(
        comodel_name='stock.production.lot',
        string='Serial #', required=False)
    bom_id = fields.Many2one(
        comodel_name='mrp.bom', string='BoM',
        ondelete='restrict', index=True,
        domain="[('product_id','=',product_id)]")
    bom_history = fields.One2many(
        'fsm.equipment.history.file.bom', 'history_file_id',
        string='Bill of Material')
    owner_ids = fields.One2many(
        'fsm.equipment.history.file.owner', 'history_file_id',
        string='Owner')
    current_owner = fields.Many2one(
        'res.partner', compute='_compute_current_owner',
        string='Current Owner', store=True, ondelete='restrict')
    owner_names = fields.Char(
        compute='_compute_owner_names',
        string='Past Owners', store=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    parent_history_file = fields.Many2one(
        'fsm.equipment.history.file',
        string="Parent History File",
        compute='_compute_parent_history_file')
    note = fields.Text(string="Note")

    @api.model
    def _get_current_owner(self, history_file):
        last_date = False
        current_owner = False
        for o in history_file.owner_ids:
            if not last_date:
                if o.date_from:
                    last_date = o.date_from
                    current_owner = o
                if o.date_until:
                    last_date = o.date_until
                    current_owner = False
            else:
                if o.date_from and o.date_from >= last_date:
                    last_date = o.date_from
                    current_owner = o
                if o.date_until and o.date_until >= last_date:
                    last_date = o.date_until
                    current_owner = False
        return current_owner

    @api.multi
    @api.depends('owner_ids', 'owner_ids.date_from', 'owner_ids.date_until')
    def _compute_current_owner(self):
        for f in self:
            f.current_owner = False
            current_owner = self._get_current_owner(f)
            if current_owner:
                f.current_owner = current_owner.partner_id
                f.equipment_id.owned_by_id = current_owner.partner_id

    @api.multi
    @api.depends('owner_ids')
    def _compute_owner_names(self):
        for f in self:
            f.owner_names = ''
            owner_ids = list(set([o.partner_id.id for o in f.owner_ids]))
            owners = self.env['res.partner'].browse(owner_ids)
            f.owner_names = ','.join(["[%s]%s" % (p.ref, p.name) for p in owners])

    @api.multi
    def _compute_parent_history_file(self):
        for hf in self:
            parent = self.env['fsm.equipment.history.file.bom'].search([('child_history_file_id', '=', hf.id),('date_removed','=',False)], order='date_added desc', limit=1)
            hf.parent_history_file = parent.history_file_id

    @api.multi
    @api.constrains('lot_id')
    def _check_lot_id_uniq(self):
        """Check that serial number and product are uniq
        """
        for history_file in self:
            if not history_file.lot_id:
                continue
            res = self.search([('lot_id', '=', history_file.lot_id.id), ('id', '!=', history_file.id)])
            if res:
                raise exceptions.ValidationError(_('There still exists an history file for this serial number.'))

    @api.model
    def create(self, values):
        if 'name' not in values:
            lot_id = values.get('lot_id', False)
            product_id = values.get('product_id', False)
            if lot_id:
                values['name'] = self.env['stock.production.lot'].browse(lot_id).name
            else:
                values['name'] = self.env['product.product'].browse(product_id).name
        res = super(FSMEquipmentHistoryFile, self).create(values)
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            for line in rec.bom_history:
                if line.child_history_file_id:
                    if not line.child_history_file_id.lot_id:
                        line.child_history_file_id.unlink()
        return super(FSMEquipmentHistoryFile, self).unlink()

    @api.onchange('product_id')
    def onchange_product_id(self):
        mrp_bom = self.env['mrp.bom']
        if self.product_id:
            bom = mrp_bom._bom_find(product=self.product_id)
            self.bom_id = bom

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if not self.name and self.lot_id:
            self.name = self.lot_id.name
        if not self.equipment_id and self.lot_id:
            self.equipment_id = self.lot_id.fsm_equipment_id

    @api.multi
    def create_equipment_history_file_bom(self):
        """
        This recursive function fill the bom_history of history files.
        """
        bom_obj = self.env['fsm.equipment.history.file.bom']
        history_file_obj = self.env['fsm.equipment.history.file']
        mrp_bom = self.env['mrp.bom']
        for hf in self:
            if hf.bom_history:
                raise exceptions.Warning(_('You have already created the bom histroy.'))
            bom = hf.bom_id or False
            if not bom:
                bom = mrp_bom._bom_find(product=hf.product_id)
                if bom:
                    hf.bom_id = bom
            if not bom:
                raise exceptions.Warning(_('History file can not be created without BoM'))
            for bl in bom.bom_line_ids:
                if bl.product_id.history_file_relevant:
                    sub_bom = mrp_bom._bom_find(product=bl.product_id)
                    values = {
                        'product_id': bl.product_id.id,
                        'history_file_id': hf.id,
                        'bom_id': sub_bom.id,
                    }
                    hf_bom = bom_obj.with_context(default_lot_id=False).create(values)
                    if sub_bom and bl.product_id.history_file_obligatory \
                            and self.env.context.get('create_hf_from_mrp', False):
                        continue
                    elif sub_bom and bl.product_id.history_file_obligatory \
                            and any(bl.product_id.history_file_relevant \
                            for bl in sub_bom.bom_line_ids):
                        sub_history_file = history_file_obj.with_context(default_lot_id=False).create({
                            'product_id': bl.product_id.id,
                            'bom_id': sub_bom.id})
                        hf_bom.child_history_file_id = sub_history_file.id
                        sub_history_file.create_equipment_history_file_bom()
        return True

    @api.multi
    def _get_all_bom_history(self):
        self.ensure_one()
        bom_history = self.bom_history
        for line in self.bom_history:
            if line.child_history_file_id:
                bom_history |= line.child_history_file_id._get_all_bom_history()
        return bom_history

    @api.multi
    def view_bom_structure(self):
        self.ensure_one()
        #whole_bom_histories = self.bom_history.ids
        whole_bom_histories = self._get_all_bom_history()
        if not whole_bom_histories:
            return False
        view_id = self.env.ref(
            "fsm_equipment_history_file.view_fsm_equipment_history_file_bom_structure_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'BoM Structure',
            'target': 'new',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'fsm.equipment.history.file.bom',
            #'context': "{'group_by': ['parent_id']}",
            'domain': "[('id','in',[" + ','.join(map(str, whole_bom_histories.ids)) + "])]",
            }

    @api.multi
    def set_current_owner(self, partner_id, date=False):
        today = fields.Date.today()
        if not partner_id:
            raise exceptions.Warning(_('You need a partner to set it as the current \
                    owner of the history file.'))
        _logger.info('set current owner of history file to %s', partner_id)
        for f in self:
            if f.current_owner:
                f.reset_current_owner()
                _logger.info('current owner reset')
            f.write({'owner_ids': [(0, 0, {'history_file_id': f.id,
                                           'partner_id': partner_id,
                                           'date_from': date or today,
                                           'date_until': False})]})

    @api.multi
    def reset_current_owner(self, partner_id=False, date=False):
        today = fields.Date.today()
        for f in self:
            if f.current_owner:
                if partner_id and partner_id != f.current_owner.id:
                    f.write({'owner_ids': [(0, 0, {'history_file_id': f.id,
                                                   'partner_id': partner_id,
                                                   'date_from': False,
                                                   'date_until': date or today})]})
                else:
                    current_owner = self._get_current_owner(f)
                    current_owner.date_until = date or today
            else:
                _logger.warning('reset owner of history file without current owner')
                if partner_id:
                    f.write({'owner_ids': [(0, 0, {'history_file_id': f.id,
                                                   'partner_id': partner_id,
                                                   'date_from': False,
                                                   'date_until': date or today})]})

class FSMEquipmentHistoryFileBom(models.Model):
    _name = 'fsm.equipment.history.file.bom'
    _description = 'FSM Equipment History File BoM'
    _order = 'name'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product',
        ondelete='restrict', index=True,
        domain="[('history_file_relevant','=',True)]")
    equipment_id = fields.Many2one(
        comodel_name='fsm.equipment',
        related="child_history_file_id.equipment_id", readonly=False,
        string='Equipment', ondelete='restrict', index=True)
    name = fields.Char(
        string='Name',
        size=128, related="product_id.display_name",
        readonly=True, store=True)
    note = fields.Text(string='Note')
    history_file_id = fields.Many2one(
        comodel_name='fsm.equipment.history.file',
        ondelete='cascade', required=True, string="Parent History File")
    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Serial Number',
        related="child_history_file_id.lot_id", readonly=False,
        ondelete='restrict', domain="[('product_id','=',product_id)]", index=True)
    bom_id = fields.Many2one(
        comodel_name='mrp.bom', string='BoM', ondelete='restrict',
        index=True, domain="[('product_id','=',product_id)]")
    date_added = fields.Date('Date added')
    date_removed = fields.Date('Date removed')
    child_history_file_id = fields.Many2one(
        comodel_name='fsm.equipment.history.file',
        ondelete='set null', string='Sub History File')
    #parent_id = fields.Many2one('fsm.equipment.history.file.bom', compute="_compute_child_ids", store=False)
    child_ids = fields.One2many(
        'fsm.equipment.history.file.bom',
        string="Child lines of the referred sub history file",
        compute='_compute_child_ids')

    @api.multi
    @api.depends('child_history_file_id')
    def _compute_child_ids(self):
        """ If the BOM line refers to a BOM, return the ids of the child BOM lines """
        for file_bom in self:
            file_bom.child_ids = file_bom.child_history_file_id.bom_history
            #for line in file_bom.child_history_file_id.bom_history:
            #    line.parent_id = file_bom

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.child_history_file_id:
                print(rec.child_history_file_id.lot_id)
                if rec.child_history_file_id.lot_id:
                    raise exceptions.UserError(_('You cannot delete the bom and its child history file with serial number.'))
                else:
                    rec.child_history_file_id.unlink()
        return super(FSMEquipmentHistoryFileBom, self).unlink()

class FSMEquipmentHistoryFileOwner(models.Model):
    _name = 'fsm.equipment.history.file.owner'
    _description = 'FSM Equipment History File Owner'

    history_file_id = fields.Many2one(
        comodel_name='fsm.equipment.history.file',
        ondelete='restrict', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', ondelete='restrict', required=True)
    date_from = fields.Date('From')
    date_until = fields.Date('Until')
    note = fields.Text(string="Note")

