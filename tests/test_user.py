import unittest
from app.models import User

class Test_User(unittest.TestCase):

    def setUp(self):
        fname = 'Collin'
        lname = 'Mutembei'
        email = 'cm@sc.io'
        login = 'cmutembei'
        utype = 1
        pword = 'testicles'

        self.user = User.objects.create(first_name = fname, last_name = lname, \
        email = email, login = login, user_type = utype, password = pword)

    def tearDown(self):
        del self.user

    def test_usernames(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.usernames(), '{0} {1}'.format(self.user.first_name, self.user.last_name))
