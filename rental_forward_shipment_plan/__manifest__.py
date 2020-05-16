# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Rental Forward Shipment Plan",
    "summary": "Rental Routing Shipment Plan",
    "version": "12.0.1.0.0",
    "category": "Rental",
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    "license": "AGPL-3",
    "depends": [
        "rental_routing",
        "shipment_plan_rental",
    ],
    "data": [
        "views/shipment_plan_view.xml",
    ],
    "installable": True,
    'auto_install': True,
}
