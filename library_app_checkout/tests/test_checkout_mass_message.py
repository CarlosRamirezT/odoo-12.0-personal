from odoo.tests.common import TransactionCase
from odoo import exceptions

class TestWizard(TransactionCase):

    # setting the variables to be used in our tests
    def setUp(self, *args, **kwargs):
        super(TestWizard, self).setUp(*args, **kwargs)
        # test setup code must be here
        # setting the user to be carry with the recordset which also test that access security is defined
        admin_user = self.env.ref('base.user_admin') # getting the admin user
        self.Checkout = self.env['library.checkout'].sudo(admin_user) # setting the admin user into the Checkout model
        self.Wizard = self.env['library.checkout.massmessage'].sudo(admin_user) # setting the admin user into the Wizard model
        # creating a member record
        a_member = self.env['library.member'].create({'name': 'Jhon'})
        self.checkout0 = self.Checkout.create({'member_id': a_member.id})

    def test_send_button(self):
        """the send button should or must create messages on checkouts"""
        # test code here
        msgs_before = len(self.checkout0.message_ids) # getting the amount of messages before execiting the send mass messages button
        wizard0 = self.Wizard.with_context(active_ids=self.checkout0.ids)
        wizard0 = self.wizard0.create({'message_body': 'Hello'})
        wizard0.send_button()
        msgs_after = len(self.checkout0.message_ids) # getting the amount of messages after the mass message sending
        self.assertEqual(msgs_after, msgs_before + 1, 'Expected one more message on the checkout.')

    # testing that exceptions are generated on properly cases
    def test_send_button_empty_body(self):
        "Send Button user exception generated on empty body"
        wizard0 = self.Wizard.create({})
        with self.assertRaises(exceptions.UserError) as e:
            wizard0.send_button() # if this doesn't raise an exception the test check will failed