# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    "name": "Rental Timeline Transport",
    "summary": "extends the rental_timeline module to show the transport order fields in the timeline popup.",
    "version": "16.0.1.0.0",
    "category": "Rental",
    "author": "Odoo Community Association (OCA)/Elego Software Solutions GmbH",
    "depends": [
        "rental_timeline",
        #'rental_transport_purchase_request',
    ],
    "data": [
        "views/product_timeline_view.xml",
    ],
    "demo": [],
    "qweb": [],
    "installable": True,
    #'auto_install': True,
    "license": "AGPL-3",
}
