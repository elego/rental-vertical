# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Rental Routing",
    "summary": "",
    "version": "11.0.1.0.0",
    "category": "Sales",
    "author": "Yu Weng <yweng@elegosoft.com>",
    "license": "AGPL-3",
    "depends": ["sale", "sale_rental", "sale_order_autoaction"],
    "data": [
        "wizards/sale_rental_route_view.xml",
        "wizards/sale_order_autoaction_view.xml",
        "views/view_order_form.xml",
        "views/sale_rental_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
