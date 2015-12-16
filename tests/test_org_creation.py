from django.test import TestCase
from django.db import IntegrityError

from faker import Factory
from app.models.user import User, UserAuthentication, Member

fake = Factory.create()

class TestOrgCreation(TestCase):

    def setUp(self):
        self.email = fake.email()
        self.name = fake.name()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user_auth = User.create_userprofile(username=self.username, user_type=1,
                                    email=self.email, password=self.password)

    def tearDown(self):
        del self.user_auth
       
    def test_create_org(self):
        """
        Tests for creation of organisations.
        Creates an organisation.
        Checks whether created organisation is an instance of User.
        Checks for membership of default user (org admin) in the members table after the organisation is created.
        Checks that the org foreign key in Member is an organisation.
        Checks for an IntegrityError when an organisation's username is not unique (case insensitive check)
        """
        admin_id = self.user_auth.id

        organisation = User.create_orgprofile(admin_id=admin_id, username=fake.user_name(), full_name=fake.name(), user_type=2)
        self.assertTrue(isinstance(organisation, User))
        # retrieve the org members from the database
        org_members = Member.objects.get(org=organisation)
        # confirm the super user is self.user_auth
        self.assertEqual(org_members.user, self.user_auth)
        # confirm self.user_auth is user_level 1 (admin member of the org)
        self.assertEqual(org_members.user_level, 1)
        # check if organisation foreign key is of user_type 2
        self.assertEqual(org_members.org.user_type, 2)
        # expect IntegrityError when organisation is created a second time (in lowercase)
        with self.assertRaises(IntegrityError):
            organisation2 = User.create_orgprofile(admin_id=admin_id, username=organisation.username.lower(), full_name=organisation.full_name, user_type=2)

    def test_add_members_org(self):
        """
        Tests for adding members to organisations.
        Organisation is created by user self.user_auth and members of varying user levels are later added.
        Checks for total members in the organisation (after member additions are made).
        Checks for failure when non admin attempts to add members.
        """
        admin_id = self.user_auth.id

        organisation = User.create_orgprofile(admin_id=admin_id, username=fake.user_name(), full_name=fake.name(), user_type=2)

        # Create users
        user1 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        user2 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        user3 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        phony_admin = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)

        
        # adding users to the org (using self.user_auth) with varying levels of organisational rights (user_level)
        self.assertTrue(
            User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=2, member=user1)
            )
        self.assertTrue(
            User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=5, member=user2)
            )
        self.assertFalse(
            User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=9, member=user2)
            )
        # adding user3 to the org (using phony_admin). Expect failure
        self.assertFalse(
            User.add_org_member(organisation=organisation, admin_id=phony_admin.id, user_level=6, member=user3)
            )
        # expect admin, user1 and user2
        member_count = Member.objects.filter(org=organisation).count()
        self.assertEqual(member_count, 3)

    def test_org_member_removal(self):
        """
        Tests the member removal process.
        Create organisation with self.user_auth as the admin.
        Add users to the organisation first, then later test if users can be removed by admin.
        Check if particular user can be removed from the same org twice (Expect failure).
        Check if non admin (phony_admin) can remove a user (Expect failure).
        Check if member count is correct after tests are run.
        """
        admin_id = self.user_auth.id

        organisation = User.create_orgprofile(admin_id=admin_id, username=fake.user_name(), full_name=fake.name(), user_type=2)

        user1 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        user2 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        user3 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        user4 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        admin2 = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)
        phony_admin = User.create_userprofile(email=fake.email(), username=fake.user_name(), password=fake.password(), user_type=1)

        # add users as members in org
        User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=4, member=user1)
        User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=3, member=user2)
        User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=7, member=user3)
        User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=3, member=user4)
        User.add_org_member(organisation=organisation, admin_id=admin_id, user_level=1, member=admin2)
        
        # test for user removal by admin of the organisation
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=admin_id, member=user1)
            )
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=admin_id, member=user2)
            )
        # test for removal of users by an alternate admin
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=admin2.id, member=user4)
            )
        # test for removal of fellow admin
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=admin_id, member=admin2)
            )

        # remove admin2 2nd time (user doesn't exist - exception will be raised)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=self.admin_id, member=admin2)
        # expect Exception when phony admin attempts to remove user3 (no privileges)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=phony_admin.id, member=user3)
        # expect Exception when admin attempts to remove member from org more than once (doesn't exist)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=admin_id, member=user2)
        # expect Exception when admin attempts to remove the only admin from org
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=admin_id, member=self.user_profile)
            
        # expect admin and user3: count = 2
        member_count = Member.objects.filter(org=organisation).count()
        self.assertEqual(member_count, 2)