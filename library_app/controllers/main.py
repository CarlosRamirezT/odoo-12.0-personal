from odoo import http

class Books(http.Controller):

    # auth refers to the route authorization mode, in this case we are indicating
    # that the user must be logged to be authorized. if we want if to allow
    # anonimous access then auth='public' parameter must be use
    # if using auth='public' the code should be sudo to elevate permissions
    # before trying to search books
    @http.route('/library/books', auth='user')
    def list(self, **kwargs):
        # access the enviroment and get a recordset with all active books
        Book = http.request.env['library.book']
        books = Book.search([])
        # process the library_app.index_template and generate the output html
        return http.request.render(
            'library_app.book_list_template', {'books': books}
        )