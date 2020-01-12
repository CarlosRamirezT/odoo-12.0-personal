from odoo import fields, models

class Book(models.Model):
    # _name is not needed at least we want to make a change to it
    # and if we do so odoo will create a new model which is a copy
    # of that model with the extended fields we add here
    _inherit = 'library.book'

    is_available = fields.Boolean(string='Is Available?')

    #
    # all atributes for these fields which were not explicitly mentioned remain unchanged
    #
    # adding text to the help dialog when the mouse hovers
    isbn = fields.Char(help='Use a valid ISBN-13 or ISBN-10.')
    # indexing the publisher_id field so searches are more efficient
    publisher_id = fields.Many2one(index=True)

