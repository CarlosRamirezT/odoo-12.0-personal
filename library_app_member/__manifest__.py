# -*- coding: utf-8 -*-
{
    'name': "Library Member Managment",

    'summary': """
        Adds functionality to manage library memebers""",

    'description': """
        It will extend the Book Model and add a flag, signaling if they are available to borrow a
        book. This information should be shown in the Book form and on the website catalogue
        page.
        
        It should add the Library Member master data Model. Members should store personal data,
        such as name, address, and email, similarly to Partners, and have specific data, such as the
        library card number. The most efficient solution is to use Delegation inheritance, where a
        Library Member record will be automatically created and contain a related Partner record.
        This solution makes all Partner fields available for Members, without data structure
        duplication.
        
        We would like to provide Members with the messaging and social features that are
        available on the borrowing form, including the planned activities widget, to allow for better
        collaboration.
        
        We plan to introduce a feature that allows Members to borrow Books from the Library, but
        it will be out of scope for now.
    """,

    'author': "Cadara Software",
    'depends': ['library_app', 'mail'],
    'data': [
        'views/book_view.xml',
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/member_view.xml',
        'views/library_menu.xml',
        'views/book_list_template.xml',
    ],
    'application': False,
}