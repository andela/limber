import unittest
import json

from random import random

from django.test import Client, TestCase

from faker import Factory

from app.models.user import User, UserAuthentication, Member

fake = Factory.create()


class TestOrgMembership(TestCase):
	"""Test all the urls for the MemberViewSet."""

	def setUp(self):
		"""initialize test resources."""
		self.client = Client()
		# a user to perform requests that require authentication
		self.user = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		# create the user in the database
		response = self.client.post('/api/user/', data=self.user)
		# login user
		response = self.client.post(
			'/api/api-auth/login/?next=/api/user/',
			data={
				'username': self.user.get('email'),
				'password': self.user.get('password')
			}
		)
		# create an organisation to which members will be added
		# the creator will be the default admin
		response = self.client.post(
			'/api/org/',
			data={
				'username': fake.user_name(),
				'full_name': fake.name()
			}
		)
		# retrieve the org object from the DB using the id in the response
		response = self.client.get('/api/member/')
		org_id = response.data[0].get('org')
		self.org_object = User.objects.get(pk=org_id)
		# create user2 whose membership to org will be tested later
		user2 = {
			'email': fake.email(),
			'username': fake.user_name(),
			'password': fake.password()
		}
		# create the second user
		response = self.client.post('/api/user/', data=user2)
		# get user2 object from the DB
		self.user2_object = User.objects.get(username=user2.get('username'))

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		del self.client
		del self.user

	def create_org_member(self):
		"""Create a member in an organisation."""
		self.user_object = UserAuthentication.objects.get(
			profile=self.user2_object
		)
		# add user2 to the organisation as an admin (user_level 1)
		response = self.client.post(
			'/api/member/',
			data={
				'org': self.org_object.id,
				'user': self.user_object.id,
				'user_level': 1
			}
		)

		return response

	def test_unauthenticated_requests(self):
		"""Test unauthenticated request to the '/api/member' url."""
		# logout first
		response = self.client.get('/api/api-auth/logout/?next=/api/')
		# unauthenticated GET
		response = self.client.get('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')
		# unauthenticated DELETE
		response = self.client.delete('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')
		# unauthenticated POST
		response = self.client.post('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')
		# unauthenticated PUT
		response = self.client.put('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_successful_post_member(self):
		"""Test successful post request to the '/api/member/' url."""
		response = self.create_org_member()

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		# View the new member. (Member 2 because of the default admin)
		member2 = Member.objects.get(user=self.user_object)
		response = self.client.get('/api/member/' + str(member2.id) + '/')
		# ensure the user id in the response is the user id in the object
		self.assertEqual(response.data.get('user'), self.user_object.id)
		# ensure the organisation id in the response
		# is the organisation id in the object
		self.assertEqual(response.data.get('org'), self.org_object.id)
		# ensure a user level of 1
		self.assertEqual(response.data.get('user_level'), 1)
		# ensure there are currently 2 members in the org
		# (default admin + user2)
		response = self.client.get('/api/member/')
		self.assertEqual(len(response.data), 2)

	def test_successful_put_member(self):
		"""Test put request to the '/api/member/' url."""
		# create a member
		response = self.create_org_member()

		user_levels = [2, 3, 4, 5, 6]
		rand = int(len(user_levels) * random())

		member2 = Member.objects.get(user=self.user_object)
		json_data = json.dumps(
			{
				'org': self.org_object.id,
				'user': self.user_object.id,
				'user_level': user_levels[rand]
			}
		)
		response = self.client.put(
			'/api/member/' + str(member2.id) + '/',
			data=json_data,
			content_type='application/json'
		)
		self.assertTrue(response.status_code, 200)
		self.assertTrue(response.status_text, 'OK')
		self.assertNotEqual(response.data.get('user_level'), 1)

	def test_successful_delete_member(self):
		"""Test delete request to the '/api/member/' url."""
		# create a member
		response = self.create_org_member()
		self.assertTrue(response.status_code, 201)
		self.assertTrue(response.status_text, 'Created')

		member2 = Member.objects.get(user=self.user_object)

		response = self.client.delete(
			'/api/member/' + str(member2.id) + '/'
		)
		self.assertTrue(response.status_code, 200)
		self.assertTrue(response.status_text, 'OK')
		response = self.client.get(
			'/api/member/' + str(member2.id) + '/'
		)
		self.assertTrue(response.status_code, 200)
		self.assertTrue(response.status_text, 'OK')
		self.assertTrue('Not found' in response.data.get('detail'))

	def test_delete_sole_admin(self):
		"""Test delete attempt on the only admin in the org."""
		# get the user_auth
		def_user = User.objects.get(username=self.user.get('username'))
		def_userauth = UserAuthentication.objects.get(profile=def_user)
		# get the member object
		def_member = Member.objects.get(user=def_userauth)
		response = self.client.delete('/api/member/' + str(def_member.id) + '/')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue('Member not removed' in response.data.get('status'))
