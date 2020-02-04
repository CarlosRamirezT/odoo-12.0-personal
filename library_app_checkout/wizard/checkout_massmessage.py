# for logging to console
import logging
_logger = logging.getLogger(__name__)

from odoo import fields, models, api, exceptions

class CheckoutMassMessage(models.TransientModel):
    _name = 'library.checkout.massmessage'
    _description = 'Send mass message to book borrowers'

    checkout_ids = fields.Many2many(
        comodel_name='library.checkout',
        string='Checkouts',
    )

    message_subject = fields.Char()
    message_body = fields.Html()

    @api.model
    def default_get(self, field_names):
        default = super().default_get(field_names)
        checkout_ids = self.env.context['active_ids']
        default['checkout_ids'] = checkout_ids
        return default

    @api.multi
    def send_button(self):
        # breakpoint to run debugger
        import pdb; pdb.set_trace()
        self.ensure_one()
        # raising exceptions if validation or bussines logic is not met
        if not self.checkout_ids:
            raise exceptions.UserError('Select checkouts to send messages.')
        if not self.message_body or self.message_body == '':
            raise exceptions.UserError('Message must have body content')
        #
        for checkout in self.checkout_ids:
            checkout.message_post(
                body=self.message_body,
                subject=self.message_subject,
                subtype='mail.mt_comment',
            )
            # logging debug to console
            #
            _logger.debug(
                'Message on {} to followers: {}'.format(
                    checkout.id,
                    checkout.message_follower_ids
                )
            )
        # logging info to console
        #
        _logger.info(
            'Posted {quantity} Messages to checkouts: {checkout_ids}'.format(
                quantity=len(self.checkout_ids),
                checkout_ids=str(self.checkout_ids)
            )
        )
        return True
