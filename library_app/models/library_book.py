from odoo import api, fields, models
from odoo.exceptions import Warning, ValidationError

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _order = 'name, date_published desc'
    # _rec_name = 'name' # indicates the field used as record description when referenced from related fields, Many2one or Many2many relation
    # _table = 'library_book # indicates the database table supporting the module which is usually leave to be set automatically by replacying the dots by underscore in model name
    # _log_access = True # specifies wether the auditory fields should be automatically created (create_uid, create_date)
    # _auto = False # indicates whether the underlying database table should be created or not, in which case the init() method should be overwritten to create the database model holder table
    # adding sql constraint
    _sql_constraints = [
        # (name, code, error)
        # ensuring the library doesn't have repeated book titles with the same publication date
        (
            'library_book_name_date_uq', # constraint identifier
            'UNIQUE (name,date_published)', # sql sintax for the constraint
            'The title and date of the book must be unique.' # error message
        ),
        # ensuring the library doesn't have publication dates in the future
        (
          'library_book_date_ck',
            'CHECK (date_published <= current_date)',
            'The publication date cannot be a future date'
        )
    ]

    name = fields.Char( # example using the most commond keyword arguments for field attributes
        'Title',
        required=True,
        default=None,
        index=True,
        help='Book cover title.',
        readonly=False,
        translate=False
    )
    isbn = fields.Char(string='ISBN')
    active = fields.Boolean(string='Active?', default=True)
    date_published = fields.Date() # date data type field
    image = fields.Binary(string='Cover')
    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        # specifies what happens when the related record is deleted (set null, restricted(prevents the deletion, cascade(will also delete this record)))
        ondelete='set null',
        # if true allows the ORM to use Sql Joins to search on this relation which will bypass security and the user might have access to fields it's not suppossed to have
        auto_join=False
        # context # a dictionary carrying information when navigating through the relationship, to set default values
        # domain # a list of tuples use to filter the records availables for this relation
    )
    author_ids = fields.Many2many(
        comodel_name='res.partner', # related model
        relation='library_book_res_partner_rel', # to manually define the third many2many relation generated table name
        colum1='a_id', # third table field for this record id (library.book record)
        colum2='p_id', # third table field for the other record id (res.partner record)
        string='Authors'
    )
    book_type = fields.Selection( # selection data type fields supported by odoo
        [
            ('paper', 'Paperback'),
            ('hard', 'Hardcover'),
            ('electronic', 'Electronic'),
            ('other', 'Other')
        ],
        'Type'
    )
    notes = fields.Text(string='Internal Notes') # text data type fields
    descr = fields.Html(string='Description') # html data type fields
    # numeric data type fields
    copies = fields.Integer(default=1)
    avg_rating = fields.Float(string='Average Rating', digits=(3, 2))
    price = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency') # res.currency implements a currecny helper
    # Date and datetime fields
    # alternative 1 - using a lambda function for trivial logic
    last_borrow_date = fields.Datetime(
        'Last Borrowed On',
        default=lambda self: fields.Datetime.now()
    )
    # alternative 2 - using a function to dinamically compute the value of the field
    # last_borrow_date = fields.Datetime(
    #     'Last Borrowed on',
    #     default = '_default_last_borrow_date'
    # )
    # def _default_last_borrow_date(self):
    #     return fields.Datetime.now()
    publisher_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Publisher Country',
        compute='_compute_publisher_country',
        # computed fields can't be searched or written to
        # defining inverse so we can writte to it
        inverse='_inverse_publisher_country',
        # defining search method so it can be search
        search='_search_publisher_country',

        # storing the value of this field
        # then it is not necessary to use a search function
        # as it is searchable like a any other stored field.
        # store=True

        # this field logic only copies a value from another
        # model which can be automatically handled by odoo
        # with all the functions we had to defined
        # see how this is usefull for more complex field chain
        # as dot can't be used in xml views
        # behind the scenes related fields are just computed fields
        # that conveniently inplement  inverse and search methods
        # related='publisher_id.country_id'

        # by default related fields are readonly
        # to enable inverse write
        readonly=False
    )

    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi  # api.multi is the default decorator for model methods, so it is possible to skip it
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
            return True

    # it is possible to pass the function to the compute attribute as a
    # callable element without the surrounding brackets but for that
    # we need to make shure the function is defined before the field
    # definition
    @api.depends('publisher_id.country_id')
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    # inverse method logic so it is possible to write to this field
    # writing on a computed field is the inverse logic of computation
    # that is the reason of the method's name
    # access control rules still apply so this write opperation will
    # only be possible if the user has write access rights to the parent
    # model
    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id

    # search function to enable search operation on a computed field
    # converting a search domain on the computed field into a search
    # domain on regular stored fields
    # a domain expression is a (fields, operator, value) tuple
    # in this case the field is self
    # this function is called whenever this compute field is found in
    # conditions of domain expression (whenever a search operation is tried)
    # receiving the operator and the value as function call parameters
    def _search_publisher_country(self, operator, value):
        return [('publisher_id.country_id', operator, value)]

    # using arbitrary python code to define field constraints
    # the validation will be triggered every time one of the
    # specified fields is altered and raise an exception if the
    # validation is not met
    @api.constrains('isbn')
    def _constrain_isbn_validation(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError('{} is not valid ISBN'.format(book.isbn))
