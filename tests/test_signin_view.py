import unittest
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import Client
from app.views import login
from app.models import User


def create_user():
    email = 'wmahad@gmail.com'
    user_name = 'wmahad'
    user_type = 1
    pword = 'password'

    user = User.objects.create(
        email=email, user_name=user_name, user_type=user_type, password=pword)
    return user


class Test_SignIn_View(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        del self.client

    def test_signin_fails_when_user_enters_wrong_credentials(self):
        user = create_user()
        new_user_params = {'username': 'wahad', 'password': 'password'}
        response = self.client.post(reverse('login'), data=new_user_params)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wrong Credentials.', response.content)
        self.assertNotIn(b'Welcome wahad', response.content)

    def test_signup_success_when_user_enters_correct_credentials(self):
        user = create_user()
        newer_user_params = {
            'username': 'wmahad', 'password': 'password'}
        response = self.client.post(
            reverse('login'), data=newer_user_params)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Wrong Credentials.', response.content)
        self.assertIn(b'Welcome wmahad', response.content)
