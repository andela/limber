from django.test import TestCase

from faker import Factory
from app.models.project import Project
from app.models.user import User

fake = Factory.create()


class TestProject(TestCase):
	"""Test project related methods."""

	def setUp(self):
		"""Initialize test resources."""
		self.project_name = fake.first_name()
		self.project_desc = fake.sentence()

		self.email = fake.email()
		self.username = fake.user_name()
		self.password = fake.password()
		self.user_type = 1

		self.user = User.create_userprofile(
			username=self.username, user_type=self.user_type,
			email=self.email, password=self.password
		)
		self.owner = User.objects.filter(
			username=self.username).first()
		self.project = Project.create_project(
			owner=self.owner, project_name=self.project_name,
			project_desc=self.project_desc
		)

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		del self.project
		del self.user

	def test_check_project_exists_method_when_you_enter_same_data(self):
		"""Test the method that checks if a project exists."""
		self.assertTrue(
			Project.check_project_exists(self.owner, self.project_name))

	def test_check_project_exists_method_when_you_enter_different_data(self):
		"""Test the method that checks if a project exists."""
		self.project_name = fake.first_name()
		self.assertFalse(
			Project.check_project_exists(self.owner, self.project_name))

	def test_add_new_project_succeeds_when_enter_different_data(self):
		"""Test creation of a project."""
		self.project_name = fake.first_name()
		self.project_desc = fake.sentence()
		project = Project.create_project(
			owner=self.owner, project_name=self.project_name,
			project_desc=self.project_desc)
		self.assertTrue(isinstance(project, Project))
		self.assertEqual(
			isinstance(project, Project), isinstance(self.project, Project))
		self.assertNotEqual(project, None)

	def test_add_new_project_fails_when_enter_same_data(self):
		"""Test one cannot add a project with a name that exists"""
		project = Project.create_project(
			owner=self.owner, project_name=self.project_name,
			project_desc=self.project_desc)
		self.assertFalse(isinstance(project, Project))
		self.assertNotEqual(isinstance(
			project, Project), isinstance(self.project, Project))
		self.assertEqual(project, None)

