from django.test import TestCase

from django.contrib.auth.models import User

from faker import Factory
from app.models import UserProfile

fake = Factory.create()


class TestUserProfileModel(TestCase):

    def setUp(self):
        self.email = fake.email()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.user_profile = UserProfile.objects.create(
            user=self.user, user_type=1)

    def tearDown(self):
        del self.user
        del self.user_profile

    def test_username_method(self):
        self.assertTrue(isinstance(self.user_profile, UserProfile))
        self.assertEqual(self.user_profile.usernames(), '{0}{1}'.format(
            self.user.username, self.user.email))

    def test_user_creation_fails_when_username_is_the_same(self):
        email = fake.email()
        self.user_profile = UserProfile.create_user(
            username=self.username, email=email, password=self.password)
        self.assertEqual(self.user_profile, None)

    def test_user_creation_fails_when_email_is_the_same(self):
        username = fake.user_name()
        self.user_profile = UserProfile.create_user(
            username=username, email=self.email, password=self.password)
        self.assertEqual(self.user_profile, None)

    def test_user_creation_fails_when_email_and_username_is_the_same(self):
        user_profile = UserProfile.create_user(
            username=self.username, email=self.email, password=self.password)
        self.assertEqual(user_profile, None)
        del user_profile

    def test_user_creation_succeeds_when_correct_data_is_passed(self):
        email = fake.email()
        password = fake.password()
        username = fake.user_name()
        user_profile = UserProfile.create_user(
            username=username, email=email, password=password)
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(isinstance(user_profile, UserProfile),
                         isinstance(self.user_profile, UserProfile))
        del user_profile
