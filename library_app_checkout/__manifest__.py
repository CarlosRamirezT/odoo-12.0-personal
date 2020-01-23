
{
    'name': "Library Book Borrowing Managment",
    'description': """Adds the ability for members to borrow books from the library""",
    'author': "Cadara Software",
    'depends': ['library_app_member'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/checkout_view.xml',
    ],
    'application': False,
}
