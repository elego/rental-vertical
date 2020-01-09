# Copyright 2019 Elego Software Solutions GmbH (http://www.elego.de/)
# @author: Yurdik Cervantes Mendoza <ycervantes@elegosoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Document Management System',
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Simple DMS for Odoo',
    'author': 'Elego Software Solutions GmbH,Odoo Community Association (OCA)',
    'website': 'https://github.com/elego/dms',
    'depends': [
        'document',
    ],
    "data": [
        "views/dms_document.xml",
    ],
    "demo": [
    ],
    'installable': True,
    'auto_install': True,
}
