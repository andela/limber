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


class TestTask(TestCase):
	"""Test the urls relating to TasksViewSet."""

	def setUp(self):
		"""initialize test resources."""
		# a user to perform requests that require authentication
		self.user = {
			'username': fake.user_name(),
			'email': fake.email(),
			'password': fake.password()
		}
		# store the user in the dattabase
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

	def create_story(self, project):
		"""Create a story within a project."""
		self.story_name = fake.name()
		# give a random status, category, points and stage each time this
		# method is called
		category = ['Feature', 'Bug', 'Chore', 'Release']
		cat_index = int(random() * len(category))
		points = [0, 1, 2, 3]
		point_index = int(random() * len(points))
		stage = ['Current', 'Backlog', 'Icebox', 'Done', 'Epics']
		stag_index = int(random() * len(stage))
		response = self.client.post(
			'/api/story/',
			data={
				'name': self.story_name,
				'status': self.randomize_status(),
				'category': category[cat_index],
				'points': points[point_index],
				'stage': stage[stag_index],
				'project': project.project_id
			}
		)
		return response

	def create_task(self, story):
		"""Create a task within a story."""
		self.task_description = fake.name()
		# give a random status to the task each time this method is called
		url = reverse('task-list')
		response = self.client.post(
			url,
			data={
				'status': self.randomize_status(),
				'description': self.task_description,
				'story': story.story_id
			}
		)
		return response

	def randomize_status(self):
		"""Use to randomize the status while creating a Story or a Task."""
		status = [
			'Unstarted', 'Started', 'Finished',
			'Delivered', 'Rejected', 'Accepted'
		]
		stat_index = int(random() * len(status))
		return status[stat_index]

	def test_unauthenticated_get(self):
		"""Attempt an unauthenticated get request to "/api/tasks/" url."""
		url = reverse('task-list')
		response = self.client.get(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_post(self):
		"""Attempt an unauthenticated post request to "/api/tasks/" url."""
		url = reverse('task-list')
		response = self.client.post(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_put(self):
		"""Attempt an unauthenticated put request to "/api/tasks/" url."""
		url = reverse('task-list')
		response = self.client.put(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_unauthenticated_delete(self):
		"""Attempt an unauthenticated get request to "/api/tasks/" url."""
		url = reverse('task-list')
		response = self.client.delete(url)
		self.assertTrue(
			'Authentication credentials were not provided'
			in response.data.get('detail')
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')

	def test_get_authenticated_no_tasks(self):
		"""
		Attempt an authenticated get request to "/api/tasks/" url
		(no tasks in system yet).
		"""
		self.login_user()
		url = reverse('task-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(len(response.data), 0)

	def test_post_authenticated(self):
		"""Attempt an authenticated post request to "/api/tasks/" url."""
		# login the user
		self.login_user()
		# create an organisation
		response = self.create_org()
		org_username = response.data.get('username')
		org = User.objects.get(username=org_username)
		# create a project with org owner
		self.create_project(org)
		# send a get request to get the project object from info in response
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
		url = reverse('task-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(len(response.data), 1)
		self.assertEqual(
			response.data[0].get('description'), self.task_description
		)

	def test_put_authenticated(self):
		"""Attempt an authenticated put request to "/api/tasks/" url."""
		# login the user
		self.login_user()
		# create an organisation
		response = self.create_org()
		org_username = response.data.get('username')
		org = User.objects.get(username=org_username)
		# create a project with org owner
		self.create_project(org)
		# send a get request to get the project object from info in response
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
		# update the task
		url = reverse('task-list')
		url += str(task.task_id) + '/'
		new_task_desc = fake.name()
		story = Story.objects.get(name=self.story_name)
		json_data = json.dumps(
			{
				'status': self.randomize_status(),
				'description': new_task_desc,
				'story': story.story_id
			}
		)
		response = self.client.put(
			url,
			data=json_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')
		self.assertNotEqual(
			response.data.get('description'), self.task_description
		)
		self.assertEqual(
			response.data.get('description'), new_task_desc
		)

	def test_delete_authenticated(self):
		"""Attempt an authenticated delete request to "/api/tasks/" url."""
		# login the user
		self.login_user()
		# create an organisation
		response = self.create_org()
		org_username = response.data.get('username')
		org = User.objects.get(username=org_username)
		# create a project with org owner
		self.create_project(org)
		# send a get request to get the project object from info in response
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
		# delete a task
		url = reverse('task-list')
		url += str(task.task_id) + '/'
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
