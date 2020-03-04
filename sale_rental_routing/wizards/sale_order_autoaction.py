from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderAutoactionWizard(models.Model):
    """
    This wizard applies some actions on sale order considering account,
    analytic account and project
    """

    _inherit = "sale.order.autoaction.wizard"

    show_rental_create_location_and_route = fields.Boolean(
        "Show Rental Create location & route"
    )
    rental_create_location_and_route = fields.Boolean(
        "Rental Create location & route", default=False
    )

    @api.model
    def get_default_show_values(self, order):
        res = super(SaleOrderAutoactionWizard, self).get_default_show_values(
            order
        )
        # set the date_expected
        if not order.warehouse_id.rental_out_location_id:
            raise UserError(
                _("No found default Route out location of warehouse.")
            )
        rental_out_location = order.warehouse_id.rental_out_location_id
        sale_rental = False
        for line in order.order_line:
            if line.rental_type == "new_rental":
                rental = self.env["sale.rental"].search(
                    [("start_order_line_id", "=", line.id)]
                )
                rental.in_move_id.write({"date_expected": line.end_date})
                sale_rental = True

        if (
            sale_rental
            and (not order.partner_shipping_id.rental_onsite_location_id
            or order.partner_shipping_id.rental_onsite_location_id.id
            == rental_out_location.id)
        ):
            res["show_rental_create_location_and_route"] = True
        return res

    @api.multi
    def action_confirm(self):
        """
        run auto action to create onsite location and route for rental
        """
        self.ensure_one()
        res = super(SaleOrderAutoactionWizard, self).action_confirm()
        if self.rental_create_location_and_route:
            self.order_id.create_and_set_rental_onsite_location_route()
