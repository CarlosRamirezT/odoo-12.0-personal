from odoo import api, fields, models
from odoo.exceptions import Warning

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _order = 'name, date_published desc'
    # _rec_name = 'name' # indicates the field used as record description when referenced from related fields, Many2one or Many2many relation
    # _table = 'library_book # indicates the database table supporting the module which is usually leave to be set automatically by replacying the dots by underscore in model name
    # _log_access = True # specifies wether the auditory fields should be automatically created (create_uid, create_date)
    # _auto = False # indicates whether the underlying database table should be created or not, in which case the init() method should be overwritten to create the database model holder table

    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a , b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi # api.multi is the default decorator for model methods, so it is possible to skip it
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
            return True

    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    author_ids = fields.Many2many('res.partner', string='Authors')
