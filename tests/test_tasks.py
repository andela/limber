import unittest
import json

from random import random

from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from faker import Factory
from app.models.user import User, UserAuthentication
from app.models.project import Project
from app.models.story import Story, Task

fake = Factory.create()

class TestTasks(TestCase):

	def setUp(self):
       	# a user to perform requests that require authentication
		self.user = {
			'username': fake.user_name(), 'email': fake.email(), 'password': fake.password()}
        # store the user in the dattabase
		self.client.post('/api/user/', data=self.user)

	def tearDown(self):
		del self.client
		del self.user

	def login_user(self):
		response = self.client.post('/api/api-auth/login/?next=/api/user/', data={'username':self.user.get('email'), 'password':self.user.get('password')})
		return response

	def create_org(self):
		self.org_username = fake.user_name()
		self.org_full_name = fake.name()
		response = self.client.post('/api/org/', data={'full_name': self.org_full_name, 'username': self.org_username} )
		return response

	def create_project(self, owner):
		self.project_name = fake.name()
		self.project_description = fake.name()
		
		response = self.client.post('/api/project/', data={'owner': owner.id, 'project_name': self.project_name, 'project_desc': self.project_description} )
		return response

	def create_story(self, project):
		self.story_name = fake.name()
		
		status = ['Unstarted', 'Started', 'Finished', 'Delivered', 'Rejected', 'Accepted']
		stat_index = int(random() * len(status))
		
		category = ['Feature', 'Bug', 'Chore', 'Release']
		cat_index = int(random() * len(category))
		
		points = [0, 1, 2, 3]
		point_index = int(random() * len(points))   		
		
		stage = ['Current', 'Backlog', 'Icebox', 'Done', 'Epics']
		stag_index = int(random() * len(stage))

		response = self.client.post('/api/story/', data={
					   										'name': self.story_name,
					   										'status': status[stat_index],
					   										'category': category[cat_index],
					   										'points': points[point_index],
					   										'stage': stage[stag_index],
					   										'project': project.project_id
   													}
   									)
		return response

	def create_task(self, story):
		self.task_description = fake.name()

		status = ['Unstarted', 'Started', 'Finished', 'Delivered', 'Rejected', 'Accepted']
		stat_index = int(random() * len(status))

		url = reverse('task-list')
		response = self.client.post(url, data={
													'status': status[stat_index],
													'description': self.task_description,
													'story': story.story_id
												}
									)
		return response

   	def test_get_task_unauthenticated(self):
   		"""
   		Attempt an unauthenticated get request to "/api/tasks/" url.
   		"""
   		url = reverse('task-list')
   		response = self.client.get(url)
   		self.assertTrue('Authentication credentials were not provided' in response.data.get('detail'))
   		self.assertEqual(response.status_code, 403)
   		self.assertEqual(response.status_text, 'Forbidden')

   	def test_get_task_authenticated_no_tasks(self):
   		"""
   		Attempt an authenticated get request to "/api/tasks/" url (no tasks in system yet).
   		"""
   		self.login_user()

   		url = reverse('task-list')
   		response = self.client.get(url)
   		self.assertEqual(response.status_code, 200)
   		self.assertEqual(response.status_text, 'OK')
   		self.assertEqual(len(response.data), 0)

   	def test_successful_create_task(self):
   		"""
   		Attempt an authenticated post request to "/api/tasks/" url.
   		"""
   		# login the user
   		self.login_user()

   		# create an organisation
   		response = self.create_org()
   		org_username = response.data.get('username')
   		org = User.objects.get(username=org_username)

   		# create a project with org owner
   		self.create_project(org)
   		# send a get request to get project object from info in response
   		response = self.client.get('/api/project/')
   		project_name = response.data[0].get('project_name')
   		project = Project.objects.get(project_name=project_name)

   		# create a story
   		response = self.create_story(project)
   		story_id = response.data.get('story_id')
   		story = Story.objects.get(story_id=story_id)

   		# create a task
   		response = self.create_task(story)
   		task_id = response.data.get('task_id')
   		task = Task.objects.get(task_id=task_id)
   		self.assertEqual(response.status_code, 201)
   		self.assertEqual(response.status_text, 'Created')
   		self.assertEqual(self.task_description, task.description)
