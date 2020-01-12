from odoo import fields, models

class Book(models.Model):
    # _name is not needed at least we want to make a change to it
    # and if we do so odoo will create a new model which is a copy
    # of that model with the extended fields we add here
    _inherit = 'library.book'

    is_available = fields.Boolean(string='Is Available?')

