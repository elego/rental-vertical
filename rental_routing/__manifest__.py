# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Rental Routing",
    "summary": "",
    "version": "12.0.1.0.0",
    "category": "Sales",
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    "license": "AGPL-3",
    "depends": ["rental_base"],
    "data": [
        "wizards/sale_rental_route_view.xml",
        "views/view_order_form.xml",
        "views/sale_rental_view.xml",
        "views/res_partner_view.xml",
        "views/stock_view.xml",
    ],
    "installable": True,
}
