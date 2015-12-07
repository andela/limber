from django.test import TestCase

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
        Checks whether created organisation is an instance of UserProfile.
        Checks for membership of default user (super admin) in the members table when organisation is created.
        """
       
        organisation = User.create_orgprofile(admin_id=self.user_auth.profile_id.id, username=fake.user_name(),
                                            full_name=fake.name(), user_type=1)
        self.assertTrue(isinstance(organisation, User))

        # retrieve the org from the database
        saved_org = Member.objects.get(org_id=organisation)

        # confirm the super user
        self.assertEqual(saved_org.user_id, self.user_auth.profile_id.id)
        self.assertEqual(saved_org.user_level, 1)

    def test_add_members_org(self):
        """
        Tests for adding members to organisations.
        Checks for total members in organisation after additions are made
        Checks for user level when adding members
        Checks for non admin failure when adding members
        """
        organisation = User.create_orgprofile(admin_id=self.user_auth.profile_id.id, username=fake.user_name(), full_name=fake.name(), user_type=1)

        user1 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user2 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user3 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        phony_admin = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)

        
        # insert user1 must be successful
        self.assertTrue(
            User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=2, member=user1)
            )
        # insert user2 must be successful
        self.assertTrue(
            User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=3, member=user2)
            )
        # expect failure when admin attempts to add member to org more than once
        self.assertFalse(
            User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=3, member=user2)
            )
        # expect failure when non-admin attempts to add members to org
        self.assertFalse(
            User.add_org_member(organisation=organisation, admin_id=phony_admin.profile_id.id,
                user_level=3, member=user3)
            )
        # expect admin, user1 and user2
        member_count = Member.objects.filter(org_id=organisation).count()
        self.assertEqual(member_count, 3)

    def test_org_member_removal(self):
        """
        Tests the member removal process.
        Create organisation with self.user_profile as the admin.
        Check if users can be removed.
        Check if particular user can be removed from the same org twice (Expects error).
        Check if non admin (phony_admin) can remove a user.
        Check if member count is accurate after tests are run.
        """

        organisation = User.create_orgprofile(admin_id=self.user_auth.profile_id.id, username=fake.user_name(), full_name=fake.name(), user_type=1)

        user1 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user2 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user3 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user4 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        admin2 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        phony_admin = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)

        # add users as members in org
        User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=2, member=user1)
        User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=3, member=user2)
        User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=2, member=user3)
        User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=3, member=user4)
        User.add_org_member(organisation=organisation, admin_id=self.user_auth.profile_id.id,
                user_level=1, member=admin2)
        
        # remove user1 must be successful
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=user1)
            )
        # remove user2 must be successful
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=user2)
            )
        # admin2 can remove user4 (because admin2 is user_level 1 in organisation)
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=admin2.profile_id.id, member=user4)
            )
        # can remove admin2 because self.user_profile is still an admin in organisation
        self.assertTrue(
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=admin2)
            )

        # remove admin2 2nd time (user doesn't exist - exception will be raised)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=admin2)
        # expect Exception when phony admin attempts to remove user3 (no privileges)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=phony_admin, member=user3)
        # expect Exception when admin attempts to remove member from org more than once (doesn't exist)
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=user2)
        # expect Exception when admin attempts to remove the only admin from org
        with self.assertRaises(Exception):
            User.remove_org_member(org=organisation, admin_id=self.user_auth.profile_id.id, member=self.user_profile)
            
        # expect admin and user3: count = 2
        member_count = Member.objects.filter(org_id=organisation).count()
        self.assertEqual(member_count, 2)