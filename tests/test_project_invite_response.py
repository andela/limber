import unittest
import json
import os

from random import random

from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from faker import Factory
from app.models.user import User, UserAuthentication
from app.models.project import Project
from app.models.story import Story, Task
from app.models.invite import ProjectInvite

fake = Factory.create()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestProjectInvite(TestCase):

	"""Test the urls relating to ProjectInviteViewset."""

	def setUp(self):
		"""initialize test resources."""
		# a user to perform requests that require authentication
		self.user = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		# create the user in the dattabase
		self.client.post('/api/user/', data=self.user)

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		del self.client
		del self.user

	def login_user(self):
		"""Log in the user initialized during setUp()."""
		response = self.client.post(
			'/api/api-auth/login/?next=/api/user/',
			data={
				'username': self.user.get('email'),
				'password': self.user.get('password')
			}
		)
		return response

	def create_project(self, owner):
		"""Create a project."""
		self.project_name = fake.name()
		self.project_description = fake.name()
		response = self.client.post(
			'/api/project/',
			data={
				'owner': owner.id,
				'project_name': self.project_name,
				'project_desc': self.project_description
			}
		)
		return response

	def random_accept_status(self):
		"""Select a random invite accept status."""
		choices = ProjectInvite.ACCEPT_CHOICES
		length = len(choices)
		rand_index = int(length * random())

		return choices[rand_index]

	def test_authenticated_user_not_found(self):
		""" Test a get request to '/api/project-invites/<invite_code' url.

			Test scenario where invite is responded to by a user who doesn't exists.
			This request is made while a user is authenticated.
		"""
		# login user
		self.login_user()
		# get the user object
		user_object = User.objects.get(username=self.user.get('username', None))
		# create a project
		self.create_project(user_object)
		# get the project object
		project_object = Project.objects.get(project_name=self.project_name)
		# create a project invite to user2
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		url = reverse('project-invites-list')
		self.client.post(
			url,
			data={
				'email': user2.get('email', None),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object
		pi = ProjectInvite.objects.get(email=user2.get('email', None))
		url += pi.invite_code + '/'
		# user 2 responds to the invite
		response = self.client.get(url)
		self.assertTrue(
			'User does not exist in the system' in response.data.get('message')
		)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')

	def test_unauthenticated_user_not_found(self):
		""" Test a get request to '/api/project-invites/<invite_code' url.

			Test scenario where invite is responded to by a user who doesn't exists.
			This request is made while nobody is authenticated.
		"""
		# login user
		self.login_user()
		# get the user object
		user_object = User.objects.get(username=self.user.get('username', None))
		# create a project
		self.create_project(user_object)
		# get the project object
		project_object = Project.objects.get(project_name=self.project_name)
		# create a project invite to user2
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		url = reverse('project-invites-list')
		self.client.post(
			url,
			data={
				'email': user2.get('email', None),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object
		pi = ProjectInvite.objects.get(email=user2.get('email', None))
		url += pi.invite_code + '/'
		# logout self.user1
		self.client.get('/api/api-auth/logout/')
		# user 2 responds to the invite
		response = self.client.get(url)
		self.assertTrue(
			'User does not exist in the system' in response.data.get('message')
		)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')

	def test_authenticated_user_found(self):
		""" Test a get request to '/api/project-invites/<invite_code' url.

			Test scenario where invite is responded to by a user who exists.
			This request is made while a user is authenticated.
		"""
		# login user
		self.login_user()
		# get the user object
		user_object = User.objects.get(username=self.user.get('username', None))
		# create a project
		self.create_project(user_object)
		# get the project object
		project_object = Project.objects.get(project_name=self.project_name)
		# create user2
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		self.client.post('/api/user/', data=user2)
		# create a project invite to user2
		url = reverse('project-invites-list')
		self.client.post(
			url,
			data={
				'email': user2.get('email', None),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object
		pi = ProjectInvite.objects.get(email=user2.get('email', None))
		url += pi.invite_code + '/'
		# user 2 responds to the invite
		response = self.client.get(url)
		self.assertTrue(
			'User exists in the system' in response.data.get('message')
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')

	def test_unauthenticated_user_found(self):
		""" Test a get request to '/api/project-invites/<invite_code' url.

			Test scenario where invite is responded to by a user who exists.
			This request is made while nobody is authenticated.
		"""
		# login user
		self.login_user()
		# get the user object
		user_object = User.objects.get(username=self.user.get('username', None))
		# create a project
		self.create_project(user_object)
		# get the project object
		project_object = Project.objects.get(project_name=self.project_name)
		# create user2
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		self.client.post('/api/user/', data=user2)
		# create a project invite to user2
		url = reverse('project-invites-list')
		self.client.post(
			url,
			data={
				'email': user2.get('email', None),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object
		pi = ProjectInvite.objects.get(email=user2.get('email', None))
		url += pi.invite_code + '/'
		# logout self.user1
		self.client.get('/api/api-auth/logout/')
		# user 2 responds to the invite
		response = self.client.get(url)
		self.assertTrue(
			'User exists in the system' in response.data.get('message')
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')