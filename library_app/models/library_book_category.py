from odoo import fields, models

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    _parent_store = True # to optimized reading on categories, must also add parent_path

    name = fields.Char(translate=True, required=True)

    # fields for the hierarchy
    parent_id = fields.Many2one(
        'library.book.category', # doing a Many2one relation with the same model
        'Parent Category',
        ondelete='restrict' # restricting the deletion of record if it has chield categories
    )
    parent_path = fields.Char(index=True) # must be added if using _parent_store = True

    # One2many relation
    # used to display all the records which have a Many2one relation with this field
    # in this case all the subcategories of this category
    # this is optional but is good practice to have this fields
    # child records which have this record as parent category
    child_ids = fields.One2many(
        'library.book.category', # the Many2one related model, in this case itself
        'parent_id', # the field holding the relation in the other model(itself)
        'Subcategories', # display string
    )

    # flexible relationships
    # using a flexible related field
    # to highlight either an author or a book within the category
    highlighted_id = fields.Reference(
        [
            ('library.book', 'Book'),
            ('res.partner', 'Author')
        ],
        'Category Highlight',
    )