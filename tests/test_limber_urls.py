import unittest
import json

from django.test import Client, TestCase

from faker import Factory

from app.models.user import User, UserAuthentication

fake = Factory.create()

# coverage run --omit="env*","limber*" manage.py test

class TestURLs(TestCase):

	def setUp(self):
		self.client = Client()

		# a user to perform requests that require authentication
		self.user = {'username':fake.user_name(), 'email': fake.email(), 'password':fake.password()}
		# store the user in the dattabase
		self.client.post('/api/user/', data=self.user)

	def tearDown(self):
		del self.client
		del self.user

	def test_api_url(self):
		response = self.client.get('/api/')
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
	
	def test_api_user_url(self):
		email = fake.email()
		password = fake.password()
		username = fake.user_name()

		# test the POST method
		response = self.client.post('/api/user/', data={'username':username, 'password':password, 'email':email})

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
		self.assertEqual(user.profile_id.username, username)

		# test the "/api/user/<user_id> url"
		# test the GET method first
		response = self.client.get('/api/user/' + str(user.profile_id.id) + '/')
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 1)
		self.assertEqual(response.data.get('username'), user.profile_id.username)

		# then test the PUT method
		alt_username = fake.user_name()
		alt_email = fake.email()
		alt_password = fake.password()

		# convert dictionary to json data for the put method
		json_data = json.dumps({'username':alt_username, 'email':alt_email, 'password':alt_password})
		response = self.client.put('/api/user/' + str(user.profile_id.id) + '/', content_type='application/json', data=json_data)
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.data.get('user_type'), 1)
		self.assertEqual(response.data.get('username'), alt_username)
		# I noticed this doesn't update the email and password from the UserAuthentication model

		# then test the DELETE method
		response = self.client.delete('/api/user/' + str(user.profile_id.id) + '/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		
		# confirm deletion from the database end
		user = UserAuthentication.objects.filter(email=email).first()
		self.assertFalse(user)
		
	def test_api_org_url(self):
		name = fake.name()
		username = fake.user_name()

		# test the POST method (unauthenticated)
		response = self.client.post('/api/org/', data={'username':username, 'full_name':name, 'user_type':2})

		# status code 403 - access Forbidden (nobody logged in)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

		# log in
		response = self.client.post('/api/api-auth/login/?next=/api/user/', data={'username':self.user.get('email'), 'password':self.user.get('password')})
		self.assertEqual(response.status_code, 302)
		
		# test the POST method (authenticated)
		response = self.client.post('/api/org/', data={'username':username, 'full_name':name, 'user_type':2})
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

		json_data = json.dumps({'username':alt_username, 'full_name':alt_fullname})
		response = self.client.put('/api/org/' + str(org_db.id) + '/', content_type='application/json', data=json_data)

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

		