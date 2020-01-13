from odoo import fields, models

# using delegation inheritance to create a member model.
# if we recall the inheritance mechanisms that oddo provides:
# - inheriting from an existing model using the same name in both name and _inherit
# allows us to make in place modifications to the models

# - inheriting from an existing model using a different name and the mention model in _inherit
# allows us to duplicate the parent model and the new model will have all the parent fields plus
# the ones we add without modifying the parent model.

# - delegation inheritance is done embedding models inside another model. in uml terms this is a
# composition relationship meaning that the child model cannot exist without the parent model but
# the parent model can exist without the child. this allows us to link to the fields in the parent
# model without duplicating data inside our database
#
# methods are not available in the child model
#
# if modifications are made on the parent model then they will be available to all the child models
# that are embedding them
#
# another approach to this will be to make a many2one field to the parent record, then override the
# create method so the parent record is also created and then create all the fields that we want from
# the parent model and make then related to their respective field in parent. Sometimes this is a better
# way to do this when we want certain fields to be used an not a full-fledged of the whole model.
# for example the res.company model does not inherit res.partner model but instead uses a res.partner
# record to store many of its fields.

# using delegation inheritance
class Member(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    card_number = fields.Char()
    # linking to the res.partner model
    # thus embeding res.partner in this model
    # when a member record is created a res.partner
    # is automatically created
    partner_id = fields.Many2one(
        'res.partner',
        delegate=True,
        ondelete='cascade',
        required=True
    )
