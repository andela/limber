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
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')

	def test_unauthenticated_post(self):
		""" Test an unauthenticated post request to '/api/project-invites/' url."""
		url = reverse('project-invites-list')
		response = self.client.post(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.status_text, 'Unauthorized')

	def test_unauthenticated_delete(self):
		""" Test an unauthenticated delete request to '/api/project-invites/' url."""
		# login user to create project
		self.login_user()
		# retrieve user object from DB
		user_object = User.objects.get(username=self.user.get('username'))
		# create project
		self.create_project(user_object)
		# get the project object from the DB
		project_object = Project.objects.get(project_name=self.project_name)
		# create invite object for user 2
		url = reverse('project-invites-list')
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		self.client.post(
			url,
			data={
				'email': user2.get('email'),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object from DB
		pi = ProjectInvite.objects.get(email=user2.get('email'))
		# logout self.user1
		self.client.get('/api/api-auth/logout/')
		# access the object and try to delete
		url += pi.invite_code + '/'
		response = self.client.delete(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.status_text, 'Unauthorized')

	def test_unauthenticated_put(self):
		""" Test an unauthenticated put request to '/api/project-invites/' url."""
		# login user to create project
		self.login_user()
		# retrieve user object from DB
		user_object = User.objects.get(username=self.user.get('username'))
		# create project
		self.create_project(user_object)
		# get the project object from the DB
		project_object = Project.objects.get(project_name=self.project_name)
		# create invite object for user 2
		url = reverse('project-invites-list')
		user2 = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		self.client.post(
			url,
			data={
				'email': user2.get('email'),
				'project': project_object.project_id
			}
		)
		# retrieve project invite object from DB
		pi = ProjectInvite.objects.get(email=user2.get('email'))
		# logout self.user1
		self.client.get('/api/api-auth/logout/')
		# access the object and try to delete
		url += pi.invite_code + '/'
		response = self.client.put(
			url,
			data={
				'email': user2.get('email'),
				'project': project_object.project_id,
				'accept': ProjectInvite.ACCEPTED
			}
		)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.status_text, 'Unauthorized')

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

			Put operation is only called to change invite accept status to ACCEPTED.
		"""
		# user logs in
		self.login_user()
		# get the user object from the database
		user_auth = UserAuthentication.objects.get(email=self.user.get('email'))
		# create a project
		self.create_project(user_auth.profile)
		# get the project object from the database
		project_object = Project.objects.get(project_name=self.project_name)
		# user sends post request to invite url (to create an invite entry
		# on the database)
		url = reverse('project-invites-list')
		# email = fake.email()
		email = user_auth.email
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
		json_data = json.dumps(
			{
				'accept': ProjectInvite.ACCEPTED,
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
		self.assertTrue(
			'Project invite accepted' in response.data.get('message')
		)

	def test_authenticated_unsuccessful_put_invalid_accept(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.
			Test put method with invalid data for accept field.
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
		# create put request to change accept status to invalid option (email)
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
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'not a valid choice' in
			response.data.get('accept')[0]
		)

	def test_authenticated_unsuccessful_put_different_email(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.

			Test an attempt to accept a project invite by a user whose email differs
			from the one that was in the invite.
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
		# try to accept invite using self.user's email
		# expect "Login email does not match invite email" error
		json_data = json.dumps(
			{
				'accept': ProjectInvite.ACCEPTED,
				'email': self.user.get('email'),
				'project': project_object.project_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'Login email does not match invited email' in
			response.data.get('message')
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

	def test_authenticated_delete_non_existent_invite(self):
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
		# this invite code doesn't exist in the DB
		new_invite_code = project_invite_obj.create_invite_code()
		# create the '/api/project-invites/<inv_code>/' url
		url += new_invite_code + '/'
		# send the delete  request
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')

	def test_authenticated_put_non_existent_project_invite(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.

			Test an attempt to accept a project invite that doesn't exist.
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
		# generate a new invite code. (Doesn't exist in the DB)
		new_invite_code = project_invite_obj.create_invite_code()
		# create the '/api/project-invites/<inv_code>/' url
		url += new_invite_code + '/'
		# try to accept the invite
		json_data = json.dumps(
			{
				'accept': ProjectInvite.ACCEPTED,
				'email': email,
				'project': project_object.project_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
		self.assertTrue(
			'Project invite not found' in
			response.data.get('detail')
		)

	def test_authenticated_put_non_existent_user(self):
		""" Test an authenticated put request to '/api/project-invites/<inv_code>/'
			url.

			Test an attempt to accept a project invite by a user who doesn't exist.
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
		# fake email creates an invite. Email is not associated with any user,
		# hence "User not found" error later while trying to accept invite.
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
		# try to accept the invite
		json_data = json.dumps(
			{
				'accept': ProjectInvite.ACCEPTED,
				'email': email,
				'project': project_object.project_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
		self.assertTrue(
			'User not found' in
			response.data.get('detail')
		)
