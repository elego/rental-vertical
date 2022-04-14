# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression


class ProductCategory(models.Model):
    _inherit = "product.category"

    show_vehicle_number = fields.Boolean(
        string="Show Vehicle Identification Number",
        help="If checked, the vehicle identification number "
        "is displayed in product form view.",
    )
    show_license_plate = fields.Boolean(
        string="Show License Plate",
        help="If checked, the license plate is displayed in " "product form view.",
    )
    show_init_regist = fields.Boolean(
        string="Show Initial Registration",
        help="If checked, the initial registration is displayed "
        "in product form view.",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    fleet_type_id = fields.Many2one(
        comodel_name="fleet.type",
        string="Fleet Type",
        ondelete="set null",
    )

    # Category special fields
    vehicle_number = fields.Char(
        string="Vehicle Identification Number (VIN)",
    )
    license_plate = fields.Char(
        string="License Plate",
    )
    init_regist = fields.Date(
        string="Initial Registration",
    )
    show_vehicle_number = fields.Boolean(
        string="Show Vehicle Identification Number",
        related="categ_id.show_vehicle_number",
    )
    show_license_plate = fields.Boolean(
        string="Show License Plate",
        related="categ_id.show_license_plate",
    )
    show_init_regist = fields.Boolean(
        string="Show Initial Registration",
        related="categ_id.show_init_regist",
    )

    # ---need to add later ----------
    # override
    # @api.model
    # def _name_search(
    #     self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    # ):
    #     res = super()._name_search(
    #         name=name,
    #         args=args,
    #         operator=operator,
    #         limit=limit,
    #         name_get_uid=name_get_uid,
    #     )
    #     args = args or []
    #     if name:
    #         domain = [
    #             "|",
    #             ("instance_serial_number_id.name", operator, name),
    #             ("license_plate", operator, name),
    #         ]
    #         record_ids = self._search(
    #             expression.AND([domain, args]),
    #             limit=limit,
    #             access_rights_uid=name_get_uid,
    #         )
    #         if record_ids:
    #             res2 = self.browse(record_ids).name_get()
    #             return list(set(res + res2))
    #     return res


class FleetType(models.Model):
    _name = "fleet.type"
    _description = "Fleet Type"

    name = fields.Char(
        string="Name",
        translate=True,
    )
