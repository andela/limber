from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError, transaction


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
            profile_id = kwargs.get('user')
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
    """this model is to contain both user and organistation related data"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=90, unique=True, blank=True)
    user_type = models.PositiveSmallIntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @classmethod
    @transaction.atomic
    def create_userprofile(cls, **kwargs):
        # Method that creates a user
        try:
            user = User.objects.create(
                username=kwargs.get('username') ,
                user_type=kwargs.get('user_type')
            )

            user_profile = UserAuthentication.objects.create_user(
                kwargs.get('email'),
                password=kwargs.get('password'),
                user=user
            )
            
            # redirect user to a differnt view
            return user_profile
        except IntegrityError:
            return None

    @classmethod
    @transaction.atomic
    def create_orgprofile(cls, **kwargs):
        # Method that creates an organistation
        try:

            org = User.objects.create(
                username=kwargs.get('username'),
                name=kwargs.get('name'),
                user_type=kwargs.get('user_type')
            )
            import ipdb
            
            user = User.objects.filter(id=kwargs.get('id')).first()

            if user:
            
                member = Member.objects.create(org_id=org, user_id=user.id, user_level=1)

                # redirect user to a differnt view
                return org
        except IntegrityError:
            return None

    @classmethod
    def add_org_member(cls, **kwargs):
        try:
            user_auth = UserAuthentication.objects.filter(email=kwargs['email']).first()

            is_admin = Member.objects.filter(org_id=kwargs['organisation'], user_level=1, 
                                            user_id=user_auth.profile_id.id)
            if is_admin:
                user_exists = Member.objects.filter(org_id=kwargs['organisation'], user_id=kwargs['member'].profile_id.id)

                if user_exists:
                    # user already exists in org
                    return None
                else:

                    member = Member.objects.create(org_id=kwargs['organisation'],
                                user_id=kwargs['member'].user_id, user_level=kwargs['user_level'])
                    return member

            else:
                return None
            
        except IntegrityError:
            return None

    @classmethod
    def remove_org_member(cls, email=None, **kwargs):
        """
        Removes members from an organisation.
        Checks if user is an admin. If so, the logic checks if there's at least one other admin
        before proceeding to delete. (Orgs must have an admin at all times)
        For non admin members, perform removal without any constraints
        """
        user_auth = UserAuthentication.objects.filter(email=email).first()

        remover_is_admin = Member.objects.filter(org_id=kwargs['org'], user_level=1,
                                    user_id=user_auth.profile_id.id)

        if remover_is_admin:
            removed_is_admin = Member.objects.filter(org_id=kwargs['org'], user_level=1,
                                    user_id=kwargs['member'].user_id)
            if removed_is_admin:
                # check if there are other admins in the org. Do not remove if this user is the
                # only admin
                admin_count = Member.objects.filter(
                                                org_id=kwargs['org'], user_level=1
                                            ).count()
                if admin_count > 1:
                    removed_is_admin.delete()
                    return True
                elif admin_count == 1:
                    raise Exception('org needs at least one admin')
            else:
                non_admin = Member.objects.filter(
                                    org_id=kwargs['org'],user_id=kwargs['member'].user_id
                                ).exclude(user_level=1)

                if non_admin:
                    non_admin.delete()
                    return True
                else:
                    # User doesn't exist
                    raise Exception("That user doesn't exist")
        else:
            raise Exception("User doesn't have sufficient rights")


class UserAuthentication(AbstractBaseUser):
    # This model is to contain user related data
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    is_admin = models.BooleanField(default=False)
    profile_id = models.ForeignKey(User, related_name="pro")
    objects = AccountManager()
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name



# previous models start from here
class Member(models.Model):
    org_id = models.ForeignKey(User)
    user_id = models.IntegerField()
    user_level = models.PositiveSmallIntegerField(blank=False)


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    owner_id = models.ForeignKey(User)
    project_name = models.CharField(blank=False, max_length=45)
    project_desc = models.CharField(blank=False, max_length=100)


class Team(models.Model):
    user_id = models.ForeignKey(User)
    project_id = models.ForeignKey(Project)
    user_level = models.PositiveSmallIntegerField(blank=False)


class Story(models.Model):
    story_id = models.IntegerField(primary_key=True)
    project_id = models.ForeignKey(Project)
    name = models.CharField(blank=False, max_length=45)
    status = models.CharField(blank=False, max_length=45)
    category = models.CharField(blank=False, max_length=100)
    points = models.PositiveSmallIntegerField(blank=False)
    attribute_name = models.CharField(max_length=100)


class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    story_id = models.ForeignKey(Story)
    status = models.CharField(blank=False, max_length=45)
    description = models.CharField(max_length=255)
