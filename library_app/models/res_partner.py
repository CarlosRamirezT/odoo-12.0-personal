from odoo import fields, models

class Partner(models.Model):
    _inherit='res.partner'

    # One2many relation
    # used to display all the records that have a Many2one relation with each record of this field
    # in this case used to display all the books published by each publisher
    published_book_ids = fields.One2many(
        comodel_name='library.book', # the Many2one related model
        inverse_name='publisher_id', # the field holding the relation on the other model
        string='Published Books'
    )

    # Many2many relation
    # used to display all the records tha have a Many2many relation with each record of this field
    # in this case used to display all the books authored by each author
    authored_book_ids = fields.Many2many(
        comodel_name='library.book', # the Many2many related model
        string='Authored Books'
    )