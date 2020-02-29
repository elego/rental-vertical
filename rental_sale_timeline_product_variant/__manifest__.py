# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Sale Timeline Product Variant',
    'summary': 'Extends the sale_rental_timeline module to show the product variant fields in the timeline product popup.',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'OCA/Elego Software Solutions GmbH',
    'depends': [
        'sale_rental_timeline',
        'rental_product_variant',
    ],
    'data': [
        'views/product_timeline_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
