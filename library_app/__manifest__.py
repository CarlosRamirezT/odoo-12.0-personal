# -*- coding: utf-8 -*-
{
    'name': "Library Managment",
    'summary': """
        Library Managment System""",

    'description': """
        Module use to manage a library with the computa
    """,
    'author': "Cadara Software",
    'website': "http://cadara.epizy.com",
    'version': '0.1',
    'depends': ['base'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'data': [
        'security/library_security.xml',
        'views/library_menu.xml',
    ],
}