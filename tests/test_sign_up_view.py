import unittest
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import Client
from app.views import register
from app.models import User


def create_user():
    email = 'wmahad@gmail.com'
    user_name = 'wmahad'
    user_type = 1
    pword = 'password'

    user = User.objects.create(
        email=email, user_name=user_name, user_type=user_type, password=pword)
    return user


class Test_SignUp_View(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        del self.client

    def test_signup_fails_when_user_already_exists(self):
        user = create_user()
        new_user_params = {'username': 'wmahad',
                           'email': 'wmahad@gmail.com', 'user_type': 1, 'password': 'password'}
        response = self.client.post(reverse('register'), data=new_user_params)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exists.', response.content)
        self.assertNotIn(b'User created successfully.', response.content)

    def test_signup_success_when_user_does_not_exist(self):
        newer_user_params = {
            'username': 'collin', 'email': 'collin@gmail.com', 'user_type': 1, 'password': 'password'}
        response = self.client.post(
            reverse('register'), data=newer_user_params)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'User already exists.', response.content)
        self.assertIn(b'User created successfully', response.content)
