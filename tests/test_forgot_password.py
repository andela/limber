import json

from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import reverse
from faker import Factory

from app.models.pass_reset import PasswordReset
from app.models.user import User


fake = Factory.create()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestPasswordReset(TestCase):
    """Test the '/api/password/reset/' route."""

    def setUp(self):
        """initialize test resources."""
        # create a user whose password will be reset
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        self.user = User.create_userprofile(
        email=self.email, user_type=1, password=self.password, username=self.username
        )

    def tearDown(self):
        """Free resources and do some housekeeping after tests are run."""
        del self.client
        del self.user

    def test_create_password_reset_with_user_id(self):
        """Test a successful POST request to '/api/password/reset/'.

        test creation of a PasswordReset entry with a user_id.
        """
        url = reverse('password-reset-list')
        data = {
            'user': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
        self.assertEqual(self.user.id, response.data.get('user'))
        # test that an entry has been created in the database
        reset_obj = PasswordReset.objects.filter(user=self.user)
        self.assertEqual(len(reset_obj), 1)

    def test_create_password_reset_with_email(self):
        """Test a successful POST request to '/api/password/reset/'.

        test creation of a PasswordReset entry with an email.
        """
        url = reverse('password-reset-list')
        data = {
            'email': self.email
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
        self.assertEqual(self.user.id, response.data.get('user'))
        # test that an entry has been created in the database
        reset_obj = PasswordReset.objects.filter(user=self.user)
        self.assertEqual(len(reset_obj), 1)

    def test_create_password_reset_non_existent_email(self):
        """Test a successful POST request to '/api/password/reset/'.

        test creation of a PasswordReset entry with an invalid email.
        """
        url = reverse('password-reset-list')
        data = {
            'email': fake.email()
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_text, 'Not Found')
        self.assertTrue(
            'User with specified email does not exist' in
            response.data.get('status')
        )

    def test_create_password_reset_invalid_user(self):
        """Test a POST request to '/api/password/reset/'.

        Test a POST request without required data.
        """
        url = reverse('password-reset-list')
        data = {}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_text, 'Bad Request')
        self.assertTrue(
            'This field may not be null' in response.data.get('user')[0]
        )

    def test_update_password_reset(self):
        """Test a successful PUT request to '/api/password/reset/'."""
        url = reverse('password-reset-list')
        # create the reset password request
        data = {
        'user': self.user.id
        }
        response = self.client.post(url, data=data)
        # get the password request code
        reset_obj = PasswordReset.objects.get(user=self.user)
        reset_code = reset_obj.reset_code
        # attempt login with old password
        # login_url = reverse('rest_framework:login')
        login_url = '/api/api-token-auth/'
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.has_key('token'))
        # logout user
        logout_url = reverse('rest_framework:logout')
        self.client.get(logout_url)
        # build the PUT url and change the password
        url += reset_code + '/'
        data = {
            'new_password': fake.password()
        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')
        self.assertTrue('reset successful' in response.data.get('detail'))
        # attempt login with old password. Should fail.
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_text, 'Bad Request')
        self.assertFalse(response.data.has_key('token'))
        self.assertTrue(
            'Unable to login with provided credentials' in
            response.data.get('non_field_errors')[0]
        )
        # attempt login with new password
        new_login_data = {
            'email': self.email,
            'password': data.get('new_password')
        }
        response = self.client.post(login_url, new_login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')
        self.assertTrue(response.data.has_key('token'))

    def test_update_password_reset_invalid_reset_code(self):
        """Test a PUT request to '/api/password/reset/:reset_ud'.

        Test a PUT request with an invalid reset_code as the reset_id.
        """
        # using sha1 because it resembles reset_codes in PasswordReset
        reset_code = fake.sha1()
        url = reverse('password-reset-list')

        url += reset_code + '/'
        data = {
            'new_password': fake.password()
        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_text, 'Not Found')
        self.assertTrue(
            'Password reset request not found' in response.data.get('status')
            )

    def test_update_password_no_new_password(self):
        """Test a PUT request to '/api/password/reset/:reset_ud'.

        Test a PUT request without new password.
        """
        url = reverse('password-reset-list')
        # create the reset password request
        data = {
        'user': self.user.id
        }
        response = self.client.post(url, data=data)
        # get the password request code
        reset_obj = PasswordReset.objects.get(user=self.user)
        reset_code = reset_obj.reset_code
        # build the PUT url
        url += reset_code + '/'
        data = {}
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_text, 'Bad Request')
        self.assertTrue('New password required' in response.data.get('status'))
