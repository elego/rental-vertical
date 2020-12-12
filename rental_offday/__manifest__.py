# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Off Day',
    'summary': 'Calculate off-days in rentals on daily basis',
    'description': '''
During short-term rentals over several days or weeks, the customer and the salesman 
agree on so called off-days. On these days the customer still have the rented products 
but usually doesn't use them and, therefore, does not pay the daily price. This is often 
the case for weekends and holidays, since there might be some legal limitations in using 
the products on these days.
In order to meet this requirement, the salesman can add off-days on sale order lines for 
products that are rentable in days. These days will not be included in price calculation.
''',
    'usage': '''
The off-days can only be used for products rentable in days.

- Create a stockable product and activate that it is rentable in days.
- Adjust its stock in location 'Rental In'.
- Create a sale order and rent out the product in days.
- Set a start and end date, e.g. for 3 weeks.
- On sale order line you will see a page 'Off-Days'.
- Choose the type 'Weekend' in order to create 'Fixed Off-Days' and you get a list with all saturdays 
  and sundays within the rental period.   
- Add some additional off-days.
- The number of off-days reduces the rental quantity and is therefore not included in price calculation.

''',
    'version': '12.0.1.0.0',
    'category': 'Rental',
    'author': 'Odoo Community Association (OCA)/Elego Software Solutions GmbH',
    'depends': [
        'rental_pricelist',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/add_offday_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'AGPL-3',
}
