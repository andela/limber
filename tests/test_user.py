import unittest
from app.models import User


class Test_User(unittest.TestCase):

    def setUp(self):
        fname = 'Collin'
        lname = 'Mutembei'
        email = 'cm@sc.io'
        user_name = 'cmutembei'
        user_type = 1
        pword = 'testicles'

        self.user = User.objects.create(first_name=fname, last_name=lname,
                                        email=email, user_name=user_name, user_type=user_type, password=pword)

    def tearDown(self):
        del self.user

    def test_usernames(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.usernames(), '{0}{1}'.format(
            self.user.user_name, self.user.email))
