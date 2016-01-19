import unittest
import json
from django.test import Client, TestCase
from faker import Factory
from app.models.user import User, UserAuthentication
from app.models.project import Project
from app.models.story import Story
from app.models import OrgInvites
from django.core import mail
fake = Factory.create()


class TestUrls(TestCase):
    ''' 
        Test Invitation of Member to an organisation via email notifiaction.
        emails are stored as EmailMessage objects in a list at django.core.mail.outbox
        https://docs.djangoproject.com/en/dev/topics/testing/#e-mail-services
    '''

    def setUp(self):
        # a user to perform requests that require authentication
        self.user = {'username': fake.user_name(), 
                     'email': fake.email(), 
                     'password': fake.password()
                     }                  
        self.org = {'username': fake.user_name()}

        # store the user in the database
        self.client.post('/api/user/', data=self.user)
        # Create dummy organisation
        self.client.post('/api/org/', data=self.org)

    def tearDown(self):
        del self.client
        del self.user

    def test_api_url(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

    def test_creat_user(self):
        # Generate credentials
        email = fake.email()
        password = fake.password()
        username = fake.user_name()
        # Register user

        response = self.client.post(
            '/api/user/', data={'username': username, 'password': password, 'email': email})
        # check if user has been created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
    def test_unauthorised_user(self):
        # Check if unauthorise user can access page
        response = self.client.get('/api/orginvite/')
        self.assertIsNot(response.status_text, 'OK')
        self.assertIsNot(response.status_code, '200')
        self.assertEqual(response.status_code, 403)

    def test_crud(self):
        # Test Login
        response = self.client.post('/api/api-auth/login/?next=/api/user/',
                                    data={'username': self.user.get('email'),
                                          'password': self.user.get('password')})
        self.assertEqual(response.status_code, 302)
        # Check if logged in user can access page
        response = self.client.get('/api/orginvite/')
        self.assertEqual(response.status_text, 'OK')
        self.assertEqual(response.status_code, 200)
        # Create Invitation
        email = fake.email()
        current_user = UserAuthentication.objects.first()
        dummy_org = User.objects.first()
        data = {"email": email , "uid": current_user.id, "org": dummy_org.id}
        response = self.client.post('/api/orginvite/', data)
        self.assertEqual(response.status_code, 201)

        # check if same info can be posted twice
        response = self.client.post('/api/orginvite/', data)
        self.assertEqual(response.status_code, 400)

        


