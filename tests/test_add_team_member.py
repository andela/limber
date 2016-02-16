from faker import Factory

from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models.project import TeamMember, Project
from app.models.user import User


factory = APIRequestFactory()
fake = Factory.create()


class TestAddteamMember(APITestCase):
	"""Test project team methods."""

	def setUp(self):
		"""Initialize test resources."""
		self.project_name = fake.first_name()
		self.project_desc = fake.sentence()

		self.email = fake.email()
		self.username = fake.user_name()
		self.username1 = fake.user_name()
		self.password = fake.password()
		self.user_type = 1

		self.create_user = User.create_userprofile(
			username=self.username, user_type=self.user_type,
			email=self.email, password=self.password)

		self.project = Project.create_project(
			owner=self.create_user.profile, project_name=self.project_name,
			project_desc=self.project_desc)

		self.team_member_data = {
			'project': self.project.project_id,
			'user_level': 1, 'user': self.create_user.id}

		self.create_second_user = User.create_userprofile(
			username=self.username1, user_type=1,
			email=fake.email(), password=self.password)

		self.diff_team_member_data = {
			'project': self.project.project_id,
			'user_level': 1, 'user': self.create_second_user.id}

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		del self.project
		del self.create_user
		del self.create_second_user

	def test_add_team_member_success(self):
		"""Ensure a user is added in the team members list."""
		url = reverse('teammember-list')
		response = self.client.post(url, self.team_member_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(TeamMember.objects.count(), 1)
		self.assertEqual(TeamMember.objects.get().user, self.create_user)

	def test_adding_same_user_to_one_project_twice_fails(self):
		"""Check that a user isn't added to the same project twice."""
		url = reverse('teammember-list')
		first_response = self.client.post(
			url, self.team_member_data, format='json')
		second_response = self.client.post(
			url, self.team_member_data, format='json')
		self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(TeamMember.objects.count(), 1)

	def test_adding_different_users_to_same_project_succeeds(self):
		"""Test that more than one user can be added to a project."""
		url = reverse('teammember-list')

		first_response = self.client.post(
			url, self.team_member_data, format='json')
		self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

		second_response = self.client.post(
			url, self.diff_team_member_data, format='json')
		self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)

		self.assertEqual(TeamMember.objects.count(), 2)
