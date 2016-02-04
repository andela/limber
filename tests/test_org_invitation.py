
from django.test import TestCase
from faker import Factory
from app.models.user import User, UserAuthentication
from app.models import OrgInvites
fake = Factory.create()


class TestUrls(TestCase):

    '''
        Test Invitation of Member to an organisation
        via email notifiaction.
        emails are stored as EmailMessage objects in
        a list at django.core.mail.outbox
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

    def test_1_api_url(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

    def test_2_creat_user(self):
        # Generate credentials
        email = fake.email()
        password = fake.password()
        username = fake.user_name()
        # Register user

        response = self.client.post(
            '/api/user/', data={'username': username,
                                'password': password,
                                'email': email})
        # check if user has been created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')

    def test_3_unauthorised_user(self):
        # Check if unauthorise user can access page
        response = self.client.get('/api/orginvite/')

        self.assertEqual(response.status_code, 200)

    def test_4_crud(self):
        # Test Login
        response = self.client.post(
            '/api/api-auth/login/?next=/api/user/',
            data={'username': self.user.get('email'),
                  'password': self.user.get('password')})
        self.assertEqual(response.status_code, 302)

        # Check if logged in user can access page
        response = self.client.get('/api/orginvite/')

        self.assertEqual(response.status_code, 200)

        # Create Invitation
        email = fake.email()
        current_user = UserAuthentication.objects.first()
        dummy_org = User.objects.first()
        data = {"email": email, "uid": current_user.id, "org": dummy_org.id}
        response = self.client.post('/api/orginvite/', data)
        self.assertEqual(response.status_code, 201)

        # check if same info can be posted twice
        response = self.client.post('/api/orginvite/', data)
        self.assertEqual(response.status_code, 400)

    def test_5_email_esponse(self):
        email = fake.email()
        current_user = UserAuthentication.objects.first()
        dummy_org = User.objects.first()
        response = self.client.post(
            '/api/api-auth/login/?next=/api/user/',
            data={'username': self.user.get('email'),
                  'password': self.user.get('password')})

        data = {"email": email, "uid": current_user.id, "org": dummy_org.id}
        response = self.client.post('/api/orginvite/', data)
        self.assertEqual(response.status_code, 201)
        invite = OrgInvites.objects.first()
        code = invite.code
        response = self.client.get(
            '/api/orginvite/{}/'.format(code))
        self.assertEqual(response.status_code, 200)
        # user is new should return 428
        response = self.client.get(
            '/api/orginvite/{}/?register=org'.format(code))
        self.assertEqual(response.status_code, 428)
        self.assertIn('email', response.data)

        # sign up user to system
        new_email = response.data['email']
        response = self.client.post(
            '/api/user/', data={'username': 'test',
                                'password': 'password',
                                'email': new_email})
        # check if user has been created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
        # check if it returns 403 for an already existing user who is not
        # logged in
        response = self.client.get(
            '/api/orginvite/{}/?register=org'.format(code))
        self.assertEqual(response.status_code, 403)
        self.assertIn('email', response.data)

        # loggin with new_email and try to add member
        response = self.client.post('/api/api-auth/login/?next=/api/user/',
                                    data={'username': new_email,
                                          'password': 'password'})
        self.assertEqual(response.status_code, 302)
        # try to add member while logged in
        response = self.client.get(
            '/api/orginvite/{}/?register=org'.format(code))
        self.assertEqual(response.status_code, 201)
        self.assertIn('org', response.data)
        self.assertIn('user', response.data)
        data = {"email": email, "uid": current_user.id, "org": dummy_org.id}
        response = self.client.post('/api/orginvite/', data)
        # check you can invite user twice to an org
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Member already belongs to Organisation', response.data['error'])
