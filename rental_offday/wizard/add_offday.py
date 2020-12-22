from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class AddOffday(models.TransientModel):
    """
    Add more off days in sale order line
    """

    _name = "add.offday"
    _description = "Add more offdays in sale order line"

    date_from = fields.Date(
        string="Date From",
        required=True,
    )
    date_to = fields.Date(
        string="Date To",
        required=True,
    )
    order_line_id = fields.Many2one(
        "sale.order.line",
        "Sale Order Line",
        required=True,
    )

    @api.model
    def default_get(self, fields):
        model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", False)
        res = {}
        if model == "sale.order.line" and active_id:
            order_line = self.env[model].browse(active_id)
            date_min = order_line.start_date
            date_max = order_line.end_date
            res["order_line_id"] = active_id
            res["date_from"] = date_min
            res["date_to"] = date_max
        return res

    @api.multi
    def action_done(self):
        self.ensure_one()
        additional_offdays = self.order_line_id.add_offday_ids.mapped("date")
        fixed_offdays = self.order_line_id.fixed_offday_ids.mapped("date")
        date_min = self.order_line_id.start_date
        date_max = self.order_line_id.end_date
        date_min_str = fields.Date.to_string(date_min)
        date_max_str = fields.Date.to_string(date_max)
        if self.date_from < date_min:
            raise UserError(_("You can not add off day earlier than %s") % date_min_str)
        if self.date_to > date_max:
            raise UserError(_("You can not add off day later than %s") % date_max_str)
        if self.date_to < self.date_from:
            raise UserError(_("Date From must be earlier than Date To"))
        name = "Offday between (%s - %s)" % (
            fields.Date.to_string(self.date_from),
            fields.Date.to_string(self.date_to),
        )
        current_date = self.date_from
        values = []
        while current_date <= self.date_to:
            if current_date not in additional_offdays:
                if self.order_line_id.fixed_offday_type == "weekend":
                    if current_date not in fixed_offdays:
                        additional_offdays.append(current_date)
                        values.append((0, 0, {"date": current_date, "name": name}))
                else:
                    additional_offdays.append(current_date)
                    values.append((0, 0, {"date": current_date, "name": name}))
            current_date = current_date + relativedelta(days=1)
        if values:
            self.order_line_id.add_offday_ids = values
            self.order_line_id.onchange_add_offday_ids()
            self.order_line_id.rental_qty_number_of_days_change()
        return {"type": "ir.actions.act_window_close"}
