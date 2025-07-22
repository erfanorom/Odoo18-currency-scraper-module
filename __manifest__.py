{
    'name': 'Currency Scraper',
    'version': '1.0',
    'category': 'Satka',
    'sequence': 1,
    'summary': 'A simple scraper to fetch currency rates',
    'description': 'This module scrapes currency rates from tgju.org.',
    'author': 'Erfan',
    'depends': ['base', 'web'],
    'data': [
    'security/ir.model.access.csv',
    'views/currency_scraper_views.xml',
    'views/currency_wallet_views.xml',
    'views/currency_transaction_views.xml',
    'views/currency_topup.xml',
    'views/currency_scraper_actions.xml',
    'views/currency_scraper_menus.xml',
    'views/currency_scraper_template.xml', 
    'data/cron.xml',
    ],
    'assets': {
    'web.assets_frontend': [
        'currency_rate/static/src/js/refresh.js',
    ],
},
    'installable': True,
    'application': True,
    'auto_install': False,
}
