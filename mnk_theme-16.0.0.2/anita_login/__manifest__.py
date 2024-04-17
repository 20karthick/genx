# -*- coding: utf-8 -*-
{
    'name': "anita_login",

    'summary': """
        Login Pages For Odoo""",

    'description': """
        Login Pages For Odoo
    """,

    'author': "openErpNext",
    'website': "https://www.openerpnext.com",

    'category': 'Theme/Backend',
    'version': '16.0.0.1',
    'license': 'OPL-1',
    'images': [
        'static/description/banner.png',
        'static/description/anita_screenshot.png'],

    'depends': ['base', 'web'],

    'data': [
        'views/webclient_templates.xml'
    ],

    'assets': {
        'web.assets_backend': [],
        "web.assets_frontend": [
            'mnk_theme-16.0.0.2/anita_login/static/scss/login.scss'
        ],
    }
}
