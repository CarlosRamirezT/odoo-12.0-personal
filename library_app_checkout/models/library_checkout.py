from odoo import api, exceptions, fields, models

class Checkout(models.Model):
    _name = 'library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    member_id = fields.Many2one(
        comodel_name='library.member',
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Librarian',
        default=lambda s: s.env.uid,
    )
    request_date = fields.Date(
        default=lambda d: fields.Date.today()
    )
    line_ids = fields.One2many(
        'library.checkout.line',
        'checkout_id',
        string='Borrowed Books',
    )

    # implementing stages
    @api.model
    def _default_stage(self):
        Stage = self.env['library.checkout.stage']
        return Stage.search([], limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2one(
        comodel_name='library.checkout.stage',
        default=_default_stage,
        group_expand=_group_expand_stage_id,
    )
    state = fields.Selection(related='stage_id.state')

    @api.onchange('member_id')
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = fields.Date.today()
            return {
                'warning': {
                    'title': 'Changed request date',
                    'message': 'Request date changed to today.'
                }
            }

    checkout_date = fields.Date(readonly=True)
    close_date = fields.Date(readonly=True)

    @api.model
    def create(self, values):
        # code before create() which should use the 'vals' dict
        if 'stage_id' in values:
            stage = self.env['library.checkout.stage']
            new_state = stage.browse(values['stage_id']).state
            if new_state == 'open':
                values['checkout_date'] = fields.Date.today()
        new_record = super().create(values)
        # code after create() which can use new_record created
        if new_record.state == 'done':
            raise exceptions.UserError(
                'Not allowed to create a checkout in the done state.'
            )
        return new_record

    @api.multi
    def write(self, values):
        # code before the write method which updates the record
        if 'stage_id' in values:
            stage = self.env['library.checkout.stage']
            new_state = stage.browse(values['stage_id']).state
            if new_state == 'open' and self.state != 'open':
                values['checkout_date'] = fields.Date.today()
            if new_state == 'done' and self.state != 'done':
                values['close_date'] = fields.Date.today()
        super().write(values)
        # code after the write method which updates the record after its values has been modified
        return True



class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'

    checkout_id = fields.Many2one(comodel_name='library.checkout')
    book_id = fields.Many2one(comodel_name='library.book')