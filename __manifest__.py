{
    'name': 'Gestion Fournitures Bureau - Import',
    'version': '1.0',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/excel_import_wizard_view.xml',
        'views/staging_article_views.xml',
        'views/staging_journal_views.xml',
        'views/staging_stock_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}
