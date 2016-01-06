import unittest
import json

from django.test import Client, TestCase

from faker import Factory

from app.models.user import User, UserAuthentication

fake = Factory.create()



class TestURLs(TestCase):
	"""Test all the urls in Limber app."""

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
		self.client.post('/api/user/', data=self.user)

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		del self.client
		del self.user

	def test_api_url(self):
		"""Test the '/api/' url."""
		response = self.client.get('/api/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')

	def test_api_user_url(self):
		"""Test the '/api/user/' url."""
		email = fake.email()
		password = fake.password()
		username = fake.user_name()

		# test the POST method
		response = self.client.post(
			'/api/user/',
			data={'username': username, 'password': password, 'email': email}
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		self.assertEqual(response.data.get('message'), 'User Created')
		self.assertEqual(response.data.get('status'), 'User Created')

		# test the GET method
		response = self.client.get('/api/user/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data[0].get('user_type'), 1)

		# test retrieval from the database
		user = UserAuthentication.objects.filter(email=email).first()
		# confirm the user exists in the database and is not a None object
		self.assertTrue(user)
		# confirm this UserAuthentication object represents user created earlier
		self.assertEqual(user.email, email)
		self.assertEqual(user.profile.username, username)

		# test the "/api/user/<user_id> url"
		# test the GET method first
		response = self.client.get('/api/user/' + str(user.profile.id) + '/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 1)
		self.assertEqual(response.data.get('username'), user.profile.username)

		# then test the PUT method
		alt_username = fake.user_name()
		alt_email = fake.email()
		alt_password = fake.password()

		# convert dictionary to json data for the put method
		json_data = json.dumps(
			{
				'username': alt_username,
				'email': alt_email,
				'password': alt_password
			}
		)
		response = self.client.put(
			'/api/user/' + str(user.profile.id) + '/',
			content_type='application/json',
			data=json_data
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 1)
		self.assertEqual(response.data.get('username'), alt_username)
		# I noticed this doesn't update the email and password
		# from the UserAuthentication model

		# then test the DELETE method
		response = self.client.delete('/api/user/' + str(user.profile.id) + '/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')

		# confirm deletion from the database end
		user = UserAuthentication.objects.filter(email=email).first()
		self.assertFalse(user)

	def test_api_org_url(self):
		"""Test the '/api/org' url."""
		name = fake.name()
		username = fake.user_name()

		# test the POST method (unauthenticated)
		response = self.client.post(
			'/api/org/',
			data={'username': username, 'full_name': name, 'user_type': 2}
		)
		# status code 403 - access Forbidden (nobody logged in)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# log in
		response = self.client.post(
			'/api/api-auth/login/?next=/api/user/',
			data={
				'username': self.user.get('email'),
				'password': self.user.get('password')
			}
		)
		self.assertEqual(response.status_code, 302)

		# test the POST method (authenticated)
		response = self.client.post(
			'/api/org/',
			data={
				'username': username,
				'full_name': name,
				'user_type': 2
			}
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		self.assertEqual(response.data.get('user_type'), 2)
		self.assertEqual(response.data.get('username'), username)
		self.assertEqual(response.data.get('full_name'), name)

		# test the GET method
		response = self.client.get('/api/org/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data[0].get('user_type'), 2)
		self.assertEqual(response.data[0].get('username'), username)
		self.assertEqual(response.data[0].get('full_name'), name)

		# test retrieval from the database
		org_db = User.objects.filter(username=username).first()

		# ensure this is not a None object
		self.assertTrue(org_db)
		# ensure the org filtered by username is the same one created earlier
		self.assertEqual(org_db.full_name, name)
		self.assertEqual(org_db.user_type, 2)

		# test the "/api/org/<org_id>" url
		# test the GET method
		response = self.client.get('/api/org/' + str(org_db.id) + '/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 2)
		self.assertEqual(response.data.get('username'), org_db.username)
		self.assertEqual(response.data.get('full_name'), org_db.full_name)

		# test the PUT method
		alt_username = fake.user_name()
		alt_fullname = fake.name()

		json_data = json.dumps({'username': alt_username, 'full_name': alt_fullname})
		response = self.client.put(
			'/api/org/' + str(org_db.id) + '/',
			content_type='application/json',
			data=json_data
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 2)
		self.assertEqual(response.data.get('username'), alt_username)
		self.assertEqual(response.data.get('full_name'), alt_fullname)

		# test the DELETE method
		response = self.client.delete('/api/org/' + str(org_db.id) + '/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')

		# confirm deletion from the database end
		org_db = User.objects.filter(username=username).first()
		self.assertFalse(org_db)

	def test_api_member_url(self):
		"""Test the '/api/member' url."""
		# test unauthenticated GET request
		response = self.client.get('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# test unauthenticated POST request
		response = self.client.post('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# test unauthenticated DELETE request
		response = self.client.delete('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# test unauthenticated PUT request
		response = self.client.put('/api/member/')
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# test a successful post request
		# first login user
		response = self.client.post(
			'/api/api-auth/login/?next=/api/user/',
			data={
				'username': self.user.get('email'),
				'password': self.user.get('password')
			}
		)
		# create an organisation to which members will be added
		# the creator will be the default admin
		org_name = fake.name()
		org_username = fake.user_name()
		response = self.client.post(
			'/api/org/',
			data={'username': org_username, 'full_name': org_name}
		)

		# retrieve the org object from the DB using the id in the response
		# then compare org.full_name with org_name
		response = self.client.get('/api/member/')
		org_id = response.data[0].get('org')
		org_object = User.objects.get(pk=org_id)
		self.assertEqual(org_name, org_object.full_name)
		# also retrieve the user object from the info in the response
		user_id = response.data[0].get('user')
		default_admin = UserAuthentication.objects.get(pk=user_id)
		self.assertEqual(self.user.get('email'), default_admin.email)
		# ensure there is only one user in the org so far (the default_admin)
		# and that he/she is admin (user_level 1)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0].get('user_level'), 1)
		# make sure the status code is ok
		self.assertTrue(response.status_code, 200)
		self.assertTrue(response.status_text, 'OK')

		# add a second member to organisation
		# first create the user to be added
		user2 = {
			'email': fake.email(),
			'username': fake.user_name(),
			'password': fake.password()
		}
		response = self.client.post('/api/user/', data=user2)

		# get the user's username from the response
		# then use that username to fetch a user object from the DB
		# this user object's id will be supplied as a foreign key
		# to the user table when adding this member
		response = self.client.get('/api/user/')
		user2_username = response.data[1].get('username')
		user_object_fk = User.objects.filter(username=user2_username)
		user_object = UserAuthentication.objects.get(profile=user_object_fk)

		# add user2 to the organisation as an admin (user_level 1)
		response = self.client.post(
			'/api/member/',
			data={'org': org_object.id, 'user': user_object.id, 'user_level': 1}
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		# View the new member.
		response = self.client.get('/api/member/2/')
		# ensure the user id in the response is the user id in the object
		self.assertEqual(response.data.get('user'), user_object.id)
		# ensure the organisation id in the response
		# is the organisation id in the object
		self.assertEqual(response.data.get('org'), org_object.id)
		# ensure a user level of 1
		self.assertEqual(response.data.get('user_level'), 1)

		# test the PUT method to update member's user level in the org
		json_data = json.dumps(
			{'org': org_object.id, 'user': user_object.id, 'user_level': 3}
		)
		response = self.client.put(
			'/api/member/2/',
			content_type='application/json',
			data=json_data
		)
		self.assertEqual(response.data.get('user_level'), 3)
		self.assertNotEqual(response.data.get('user_level'), 1)

		# test the DELETE method
		response = self.client.delete('/api/member/2/')
		self.assertTrue('Member successfully removed' in response.data.get('status'))
		# try to access after delete - expect 404
		response = self.client.get('/api/member/2/')
		self.assertTrue('Not found' in response.data.get('detail'))
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
		# test delete on the only remaining admin in the org - this should not happen
		response = self.client.delete('/api/member/1/')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue('Member not removed' in response.data.get('status'))
