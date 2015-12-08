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

	def setUp(self):
		self.project_name = fake.first_name()
		self.project_desc = fake.sentence()

		self.email = fake.email()
		self.username = fake.user_name()
		self.username1 = fake.user_name()
		self.password = fake.password()
		self.user_type = 1


		self.create_user = User.create_userprofile(username=self.username,
			user_type=self.user_type, email=self.email, password=self.password)

		self.user = User.objects.filter(username=self.username).first()

		self.project = Project.create_project(owner=self.user,
			name=self.project_name, desc=self.project_desc)

		self.team_member_data = {'project' : self.project.project_id,
		'user_level' : 1, 'user' : self.user.id}

		self.create_second_user = User.create_userprofile(username=self.username1,
			user_type=1, email=fake.email(), password=self.password)

		self.second_user = User.objects.filter(username=self.username1).first()

		self.diff_team_member_data = {'project' : self.project.project_id,
		'user_level' : 1, 'user' : self.second_user.id}





	def tearDown(self):
		del self.project
		del self.user

	def test_add_team_member_success(self):
		"""
		Ensure a user is added in the team members list
		"""
		url = reverse('teammember-list')
		response = self.client.post(url, self.team_member_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(TeamMember.objects.count(), 1)
		self.assertEqual(TeamMember.objects.get().user, self.user)


	def test_adding_same_user_to_one_project_twice_fails(self):
		"""
		Check that a user isn't added to the same project twice.
		"""
		url = reverse('teammember-list')
		first_response = self.client.post(url, self.team_member_data, format='json')
		second_response = self.client.post(url, self.team_member_data, format='json')
		self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(TeamMember.objects.count(), 1)


	def test_adding_different_users_to_same_project_succeeds(self):
		"""
		Tests that more than one user can be added to a project.
		"""

		url = reverse('teammember-list')

		first_response = self.client.post(url, self.team_member_data, format='json')
		self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

		second_response = self.client.post(url, self.diff_team_member_data, format='json')
		self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)

		self.assertEqual(TeamMember.objects.count(), 2)
