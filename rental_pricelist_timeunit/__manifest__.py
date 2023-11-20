# -*- coding: utf-8 -*-
{
    'name': "Rental pricelist by time unit",

    'summary': """Changes the behavior of rental_pricelist so that it makes discounts for the number of days/weeks/months and not for the number of time units multiplied by the units""",
    'description': """Change the behavior of rental_pricelist so that it makes discounts for the number of days/weeks/months and not for the number of time units multiplied by the units, in contexts in which large quantities are rented
	 and the aim is to encourage long-term rentals, so important is only the duration of the rental and not the units.
	""",
    "category": "Rental",
    'author': "zvERP, elego Software Solutions GmbH, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/vertical-rental",

    "version": "15.0.1.0.0",

    'depends': ['base', 'rental_pricelist'],

    'data': [],
    'demo': [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
