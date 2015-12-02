from django.test import TestCase

from django.contrib.auth.models import User

from faker import Factory
from app.models import User, UserAuthentication, Member

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
       
        organisation = User.create_orgprofile(email=self.user_auth.email, username=fake.user_name(),
                                            name=fake.name(), user_type=1)

        self.assertTrue(isinstance(organisation, User))

        # retrieve the org from the database
        saved_org = Member.objects.get(org_id=organisation)

        # confirm the super user
        self.assertEqual(saved_org.user_id, self.user_auth.profile_id.id)
        self.assertEqual(saved_org.user_level, 1)

    def test_add_members_org(self):
        """
        Tests for adding members to organisations.
        Checks for total members in organisation after adding two at a time
        Checks for user level when adding members
        Checks for non admin failure when adding members
        """
        organisation = User.create_orgprofile(id=self.user_auth.profile_id.id, username=fake.user_name(), name=fake.name(), user_type=1)

        user1 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user2 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        user3 = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)
        phony_admin = User.create_userprofile(email=fake.email(), username=fake.user_name(),
            password=fake.password(), user_type=1)

        import ipdb
        ipdb.set_trace()

        # insert user1 must be successful
        self.assertTrue(
            User.add_org_member(organisation=organisation, email=self.user_auth.email,
                user_level=2, member=user1)
            )
        # insert user2 must be successful
        self.assertTrue(
            User.add_org_member(organisation=organisation, email=self.user_auth.email,
                user_level=3, member=user2)
            )
        # expect failure when admin attempts to add member to org more than once
        self.assertFalse(
            User.add_org_member(organisation=organisation, email=self.user_auth.email,
                user_level=3, member=user2)
            )
        # expect failure when non-admin attempts to add members to org
        self.assertFalse(
            User.add_org_member(organisation=organisation, email=phony_admin.email,
                user_level=3, member=user3)
            )
        # expect admin, user1 and user2
        member_count = Member.objects.filter(org_id=organisation).count()
        self.assertEqual(member_count, 3)

    # def test_org_member_removal(self):
    #     """
    #     Tests the member removal process.
    #     Create organisation with self.user_profile as the admin.
    #     Check if users can be removed.
    #     Check if particular user can be removed from the same org twice (Expects error).
    #     Check if non admin (phony_admin) can remove a user.
    #     Check if member count is accurate after tests are run.
    #     """

    #     organisation = UserProfile.create_org(username=fake.user_name(), first_name=fake.name(),
    #         city='Niamey', country='Niger', creator=self.user_profile)

    #     user1 = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())
    #     user2 = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())
    #     user3 = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())
    #     user4 = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())
    #     admin2 = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())
    #     phony_admin = UserProfile.create_user(email=fake.email(), username=fake.user_name(),
    #         password=fake.password())

    #     # add users as members in org
    #     UserProfile.add_org_member(organisation=organisation, admin=self.user_profile,
    #                              user_level=2, member=user1)
    #     UserProfile.add_org_member(organisation=organisation, admin=self.user_profile,
    #                              user_level=3, member=user2)
    #     UserProfile.add_org_member(organisation=organisation, admin=self.user_profile,
    #                              user_level=2, member=user3)
    #     UserProfile.add_org_member(organisation=organisation, admin=self.user_profile,
    #                              user_level=2, member=user4)
    #     UserProfile.add_org_member(organisation=organisation, admin=self.user_profile,
    #                              user_level=1, member=admin2)
        

    #     # remove user1 must be successful
    #     self.assertTrue(
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=user1)
    #         )
    #     # remove user2 must be successful
    #     self.assertTrue(
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=user2)
    #         )
    #     # admin2 can remove a user4 (being user_level admin and all...)
    #     self.assertTrue(
    #         UserProfile.remove_org_member(org=organisation, admin=admin2, member=user4)
    #         )
    #     # remove admin2
    #     self.assertTrue(
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=admin2)
    #         )

    #     # remove admin2 2nd time(user doesn't exist)
    #     with self.assertRaises(Exception):
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=admin2)
    #     # expect Exception when phony admin attempts to remove user(no privileges)
    #     with self.assertRaises(Exception):
    #         UserProfile.remove_org_member(org=organisation, admin=self.phony_admin, member=user3)
    #     # expect Exception when admin attempts to remove member from org more than once (doesn't exist)
    #     with self.assertRaises(Exception):
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=user2)
    #     # expect Exception when admin attempts to remove the only admin from org
    #     with self.assertRaises(Exception):
    #         UserProfile.remove_org_member(org=organisation, admin=self.user_profile, member=self.user_profile)
            
    #     # expect admin and user3: count = 2
    #     member_count = Member.objects.filter(org_id=organisation).count()
    #     self.assertEqual(member_count, 2)