from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError, transaction

# from app.case_insensitive_validator import validate_case
import model_field_custom


class AccountManager(BaseUserManager):
    class Meta:
        app_label = 'app'

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
            profile = kwargs.get('user')
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class User(models.Model):
    """this model is to contain both user and organistation related data
    """

    class Meta:
        app_label = 'app'

    id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=70, unique=True)
    username = model_field_custom.CharFieldCaseInsensitive(max_length=70, unique=True)
    full_name = models.CharField(max_length=90, blank=True)
    user_type = models.PositiveSmallIntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_name(self):
        return self.username

    @classmethod
    @transaction.atomic
    def create_userprofile(cls, **kwargs):
        # Method that creates a user
        user = User.objects.create(
            username=kwargs.get('username') ,
            user_type=kwargs.get('user_type')
        )

        user_profile = UserAuthentication.objects.create_user(
            kwargs.get('email'),
            password=kwargs.get('password'),
            user=user
        )
        return user_profile

    @classmethod
    @transaction.atomic
    def create_orgprofile(cls, admin_id, **kwargs):
        # Method that creates an organistation
        org = User.objects.create(
            username=kwargs.get('username'),
            full_name=kwargs.get('full_name'),
            user_type=kwargs.get('user_type')
        )
        
        user = UserAuthentication.objects.filter(id=admin_id).first()

        # confirm the admin exists, then add him/her as default admin
        if user:
            member = Member.objects.create(org=org, user=user, user_level=1)
            return org
       
    @classmethod
    def add_org_member(cls, **kwargs):
        
        user = UserAuthentication.objects.filter(id=kwargs['admin_id']).first()
        # check if user exists
        if user:
            # check if the user is an admin in org
            is_admin = Member.objects.filter(org=kwargs['organisation'], user_level=1, 
                                        user=user)
            if is_admin:
                # check if person being added already exists in the org
                user_exists = Member.objects.filter(org=kwargs['organisation'], user=kwargs['member'])

                if user_exists:
                    # user already exists as member in org
                    return None
                else:
                    # add the person as a member in the org
                    member = Member.objects.create(org=kwargs['organisation'],
                                user=kwargs['member'], user_level=kwargs['user_level'])
                    return member
            # the is_admin is not an admin
            return None
        else:
            # user doesn't exist in the DB
            return None

        

    @classmethod
    def remove_org_member(cls, **kwargs):
        """
        Removes members from an organisation.
        Checks if user is an admin. If so, the logic checks if there's at least one other admin
        before proceeding to delete. (Orgs must have an admin at all times)
        For non admin members, perform removal without any constraints
        """
        #check if user carrying out this operation exists in DB
        user_auth = UserAuthentication.objects.filter(id=kwargs['admin_id']).first()

        if user_auth:
            remover_is_admin = Member.objects.filter(org=kwargs['org'], user_level=1,
                                    user=user_auth)

            if remover_is_admin:
                # check if user being removed is an admin
                removed_is_admin = Member.objects.filter(org=kwargs['org'], user_level=1,
                                        user=kwargs['member'])
                if removed_is_admin:
                    # check if there are other admins in the org. Do not remove if this user is the
                    # only admin
                    admin_count = Member.objects.filter(
                                                    org=kwargs['org'], user_level=1
                                                ).count()
                    if admin_count > 1:
                        removed_is_admin.delete()
                        return True
                    elif admin_count == 1:
                        raise Exception('org needs at least one admin')
                else:
                    non_admin = Member.objects.filter(
                                        org=kwargs['org'],user=kwargs['member']
                                ).exclude(user_level=1)

                    if non_admin:
                        non_admin.delete()
                        return True
                    else:
                        # User doesn't exist
                        raise Exception("That user doesn't exist")
            else:
                raise Exception("User doesn't have sufficient rights")
        else:
            raise Exception("The id of the user trying to remove members from org is not valid")


class UserAuthentication(AbstractBaseUser):
    '''This model is to contain user related data
    '''

    class Meta:
        app_label = 'app'

    # email = models.EmailField(unique=True)
    email = model_field_custom.EmailFieldCaseInsensitive(unique=True)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    is_admin = models.BooleanField(default=False)
    profile = models.ForeignKey(User, related_name="pro")
    objects = AccountManager()
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_email(self):
        return self.email


class Member(models.Model):
    class Meta:
        app_label = 'app'
        
    org = models.ForeignKey(User)
    user = models.ForeignKey(UserAuthentication)
    user_level = models.PositiveSmallIntegerField(blank=False)