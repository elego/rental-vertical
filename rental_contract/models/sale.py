# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_start = fields.Date(related="start_date", store=True)
    date_end = fields.Date(related="end_date", store=True)

    @api.onchange("end_date")
    def end_date_change(self):
        super().end_date_change()
        if self.end_date:
            self.date_end = self.end_date

    @api.onchange("start_date")
    def start_date_change(self):
        super().start_date_change()
        if self.start_date:
            self.date_start = self.start_date

    @api.onchange("date_start", "date_end", "product_uom")
    def onchange_contract_date_start_end(self):
        if self.date_start and self.date_end and not self.rental:
            number = self._get_number_of_time_unit()
            if number:
                self.product_uom_qty = number

    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        res = super()._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id
        )
        if self.product_id.income_analytic_account_id:
            res["analytic_account_id"] = self.product_id.income_analytic_account_id.id
        return res

    def update_start_end_date(self, date_start, date_end):
        super().update_start_end_date(date_start, date_end)
        for line in self:
            if line.is_contract and line.contract_id:
                contract_lines = line.contract_id.contract_line_ids.with_context(
                    no_date_checks=True
                ).filtered(lambda x: x.sale_order_line_id.id == line.id)
                for cl in contract_lines:
                    cl.write(
                        {
                            "recurring_next_date": date_end,
                            "date_start": date_start,
                            "date_end": date_end,
                        }
                    )
                    cl._onchange_date_start()
                    if cl.last_date_invoiced and cl.date_end <= cl.last_date_invoiced:
                        cl.recurring_next_date = False

    @api.model_create_multi
    def create(self, values):
        """
        When creating new sale order lines, when order state is 'sale',
        contract lines have to be added in existing or new contract, too.
        :param vals_list: dictionary
        :return: sale.order.line objects
        """
        so_lines = super().create(values)
        for sol in so_lines:
            if sol.product_id and sol.order_id.state == "sale":
                if (
                    sol.product_id.is_contract
                    and sol.product_id.property_contract_template_id
                ):
                    contracts = (
                        self.env["contract.line"]
                        .search(
                            [
                                (
                                    "sale_order_line_id",
                                    "in",
                                    sol.order_id.order_line.ids,
                                ),
                            ]
                        )
                        .mapped("contract_id")
                        .filtered(
                            lambda c: c.contract_template_id
                            == sol.product_id.property_contract_template_id
                            and c.date_end >= sol.start_date
                        )
                    )
                    if contracts:
                        sol.create_contract_line(contracts[0])
                        sol.write({"contract_id": contracts[0].id})
                    else:
                        sol.order_id.action_create_contract()
        return sol


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_contract_value(self, contract_template):
        res = super()._prepare_contract_value(contract_template)
        so_rental_order = self.env.ref("rental_base.rental_sale_type")
        customer_contract = self.env.ref("rental_contract.customer_contract_type")
        customer_rental_contract = self.env.ref(
            "rental_contract.customer_rental_contract_type"
        )
        type_id = False
        if res:
            if self.type_id.id == so_rental_order.id:
                type_id = customer_rental_contract
            else:
                type_id = customer_contract
            res.update(
                {
                    "type_id": type_id.id if type_id else False,
                    "sale_type_id": self.type_id.id,
                }
            )
        return res

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.type_id:
            res["sale_type_id"] = self.type_id.id
        return res
