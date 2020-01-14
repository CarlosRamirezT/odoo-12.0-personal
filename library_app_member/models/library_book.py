from odoo import api, fields, models

class Book(models.Model):
    # _name is not needed at least we want to make a change to it
    # and if we do so odoo will create a new model which is a copy
    # of that model with the extended fields we add here
    _inherit = 'library.book'

    is_available = fields.Boolean(string='Is Available?')

    # extending the _check_isbn() method to support 10 digit isbn
    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 10:
            ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            total = sum(a * b for a, b in zip(digits[:9], ponderators))
            check = total % 11
            return digits[-1] == check
        else:
            return super()._check_isbn

    # adding text to the help dialog when the mouse hovers
    # all atributes for these fields which were not explicitly mentioned remain unchanged
    #
    isbn = fields.Char(help='Use a valid ISBN-13 or ISBN-10.')
    # indexing the publisher_id field so searches are more efficient
    publisher_id = fields.Many2one(index=True)

