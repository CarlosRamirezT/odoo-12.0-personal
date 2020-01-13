from odoo.tests.common import TransactionCase

class TestBook10(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)

        # setting up the test enviroment user to admin
        # to test the security
        # as the default user used for tests is __system__
        # which bypasses all security
        user_admin = self.env.ref('base.user_admin')
        self.env = self.env(user=user_admin)

        self.Book = self.env['library.book']
        self.book_ode = self.Book.create({
            'name': 'Lord of the Flies',
            'isbn': '0-571-05686-5'
        })
        return result

    def test_create(self):
        "Test Books are active by default"
        self.assertEqual(self.book_ode.active, True)

    def test_check_isbn_10(self):
        "Check valid ISBN"
        self.assertTrue(self.book_ode._check_isbn)


