import unittest
import json
from django.test import Client, TestCase
from faker import Factory
from app.models.user import User, UserAuthentication
from app.models.project import Project
from app.models.story import Story

fake = Factory.create()


class TestUrls(TestCase):

    def setUp(self):
        # a user to perform requests that require authentication
        self.user = {
            'username': fake.user_name(), 'email': fake.email(), 'password': fake.password()}
        # store the user in the dattabase
        self.client.post('/api/user/', data=self.user)

    def tearDown(self):
        del self.client
        del self.user

    def test_api_url(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

    def test_api_stories(self):
        # Generate credentials
        email = fake.email()
        password = fake.password()
        username = fake.user_name()
        # Register user

        response = self.client.post(
            '/api/user/', data={'username': username, 'password': password, 'email': email})
        # check if user has been created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')

        # Check if unauthorise user can access page
        response = self.client.get('/api/story/')
        self.assertIsNot(response.status_text, 'OK')
        self.assertIsNot(response.status_code, '200')
        self.assertEqual(response.status_code, 403)

        # log in using fake user
        response = self.client.post('/api/api-auth/login/?next=/api/user/',
                                    data={'username': self.user.get('email'),
                                          'password': self.user.get('password')})
        self.assertEqual(response.status_code, 302)

        # Check if logged in user can access page
        response = self.client.get('/api/story/')
        self.assertEqual(response.status_text, 'OK')
        self.assertEqual(response.status_code, 200)

        # create project
        owner = User.objects.all().first()
        project_name = fake.name()
        project_desc = fake.name()
        response = self.client.post(
            '/api/project/', data={"owner": owner.id, "project_name": project_name, "project_desc": project_desc})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')

        # Create story
        project = Project.objects.filter(owner=owner.id).first()
        name = fake.name()
        status = fake.name()
        category = fake.name()
        points = 1
        stage = fake.name()
        response = self.client.post('/api/story/', data={'project': project.project_id,
                                                         'name': name,
                                                         'status': status,
                                                         'category': category,
                                                         'points': points,
                                                         'stage': stage,
                                                         }
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
        # retrieve story from Database
        story = Story.objects.filter(project=project.project_id).first()
        # Check if retrieved data tallies with what is sent
        response = self.client.get('/api/story/{}/'.format(story.story_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), story.name)
        self.assertEqual(response.data.get('status'), story.status)

        # Test Updating
        new_name = fake.name()
        new_stage = fake.name()
        data = {
            'name': new_name,
            'stage': new_stage,
            'category': response.data.get('category'),
            'points': response.data.get('points'),
            'status': response.data.get('status'),
            'project': response.data.get('project')
        }

        json_data = json.dumps(data)

        response = self.client.put('/api/story/{}/'.format(story.story_id),
                                   content_type='application/json', data=json_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')
        # Make sure the data has changed nd not equal to old one
        self.assertIsNot(response.data.get('name'), name)
        self.assertEqual(response.data.get('name'), new_name)
        self.assertEqual(response.data.get('stage'), new_stage)

        response = self.client.delete('/api/story/{}/'.format(story.story_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.status_text, 'No Content')
        story_id = Story.objects.filter(story_id=story.story_id).first()
        self.assertIsNone(story_id)
