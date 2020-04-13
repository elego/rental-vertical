# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Timeline Repair',
    'summary': 'extends the rental_timeline module to show the repair orders in the timeline.',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'rental_timeline',
        'rental_repair',
    ],
    'data': [
        'views/product_timeline_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'AGPL-3',
}
