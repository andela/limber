import unittest


class TestUserManagement(unittest.TestCase):
	"""Test user related methods"""

	def setUp(self):
		"""Initialize test resources."""
		# initialize test database
		pass

	def tearDown(self):
		"""Free resources and do some housekeeping after tests are run."""
		# destroy test database
		pass

	def test_user_creation(self):
		"""Testing user creation process."""
		# create a user mandela
		# test for creation by retrieving his/her id from user table in DB
		pass

	def test_organisation_creation(self):
		"""Testing organisation creation process."""
		# create organisation1 with user mandela
		# test for creation by retrieving organisation1's id from user table in DB
		# check for super_admin to be user mandela

		# create a organisation2 with user mandela
		# test for creation by retrieving organisation2's id from user table in DB
		# check for super_admin to be user mandela

		# attempt to create a third organisation as either organisation1 or
		# organisation2
		# expect error

		# test for user mandela's membership in both organisations
		# test for unique organisation names. Expect error if name is same
		pass

	def test_project_ownership(self):
		"""Testing user capability to own more than one project."""
		# create project1 with mandela as owner
		# create project2 with mandela as owner

		# create project3 with organisation1 as owner
		# create project4 with organisation1 as owner
		pass

	suite = unittest.TestLoader().loadTestsFromTestCase(TestUserManagement)
	unittest.TextTestRunner(verbosity=2).run(suite)
