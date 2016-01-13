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

	def create_org(self):
		"""Create an organisation."""
		self.org_username = fake.user_name()
		self.org_full_name = fake.name()
		response = self.client.post(
			'/api/org/',
			data={
				'full_name': self.org_full_name,
				'username': self.org_username
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

	def test_unauthenticated_get(self):
		""" Test an unauthenticated get request to '/api/project-invites/' url."""
		url = reverse('project-invites-list')
		response = self.client.get(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_post(self):
		""" Test an unauthenticated post request to '/api/project-invites/' url."""
		url = reverse('project-invites-list')
		response = self.client.post(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_delete(self):
		""" Test an unauthenticated delete request to '/api/project-invites/' url."""
		url = reverse('project-invites-list')
		response = self.client.delete(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_put(self):
		""" Test an unauthenticated put request to '/api/project-invites/' url."""
		url = reverse('project-invites-list')
		response = self.client.put(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_authenticated_get(self):
		""" Test an authenticated get request to '/api/project-invites/' url."""
		# user logs in
		self.login_user()
		# user accesses the url
		url = reverse('project-invites-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')

	def test_authenticated_post(self):
		""" Test an authenticated post request to '/api/project-invites/' url."""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_object = User.objects.get(username=self.user.get('username'))
		# create a project
		self.create_project(user_object)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url
		url = reverse('project-invites-list')
		email = fake.email()
		response = self.client.post(
			url,
			data={
				'email': email,
				'project': project_object.project_id
			}
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertTrue(
			'An invitation email has been sent'
			in response.data.get('message')
		)

	def test_authenticated_unsuccessful_post(self):
		""" Test an authenticated unsuccessful post request to
			'/api/project-invites/' url.
		"""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_object = User.objects.get(username=self.user.get('username'))
		# create a project
		self.create_project(user_object)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url
		url = reverse('project-invites-list')
		# generate a name instead of an email
		email = fake.name()
		response = self.client.post(
			url,
			data={
				'email': email,
				'project': project_object.project_id
			}
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'Invalid data'
			in response.data.get('message')
		)

	def test_authenticated_put(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.
		"""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_object = User.objects.get(username=self.user.get('username'))
		# create a project
		self.create_project(user_object)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url (and create an invite record
		# on the database)
		url = reverse('project-invites-list')
		email = fake.email()
		response = self.client.post(
			url,
			data={
				'email': email,
				'project': project_object.project_id
			}
		)
		# get the projectinvite object from the database
		project_invite_obj = ProjectInvite.objects.get(
			project=project_object.project_id
		)
		# create the '/api/project-invites/<inv_code>/' url
		url += project_invite_obj.invite_code + '/'
		# create put request to change accept status
		new_status = self.random_accept_status()
		json_data = json.dumps(
			{
				'accept': new_status[0],
				'email': email,
				'project': project_object.project_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(new_status[0], response.data.get('accept'))

	def test_authenticated_unsuccessful_put(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.
		"""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_object = User.objects.get(username=self.user.get('username'))
		# create a project
		self.create_project(user_object)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url (and create an invite record
		# on the database)
		url = reverse('project-invites-list')
		email = fake.email()
		response = self.client.post(
			url,
			data={
				'email': email,
				'project': project_object.project_id
			}
		)
		# get the projectinvite object from the database
		project_invite_obj = ProjectInvite.objects.get(
			project=project_object.project_id
		)
		# create the '/api/project-invites/<inv_code>/' url
		url += project_invite_obj.invite_code + '/'
		# create put request to change accept status to invalid option
		new_status = fake.email()
		json_data = json.dumps(
			{
				'accept': new_status,
				'email': email,
				'project': project_object.project_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		# import ipdb; ipdb.set_trace()
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'is not a valid choice' in
			response.data.get('accept')[0]
		)

	def test_authenticated_delete(self):
		""" Test an authenticated delete request
			to '/api/project-invites/<inv_code>/' url.
		"""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_object = User.objects.get(username=self.user.get('username'))
		# create a project
		self.create_project(user_object)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url (and create an invite record
		# on the database)
		url = reverse('project-invites-list')
		email = fake.email()
		response = self.client.post(
			url,
			data={
				'email': email,
				'project': project_object.project_id
			}
		)
		# get the projectinvite object from the database
		project_invite_obj = ProjectInvite.objects.get(
			project=project_object.project_id
		)
		# create the '/api/project-invites/<inv_code>/' url
		url += project_invite_obj.invite_code + '/'
		# send the delete  request
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		# expect 404 not found after delete
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
