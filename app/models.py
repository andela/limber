from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_type = models.PositiveSmallIntegerField(blank=False)
    city = models.CharField(max_length=70)
    country = models.CharField(max_length=45)

    def usernames(self):
        return '{0}{1}'.format(self.user.username, self.user.email)

    @classmethod
    def create_user(cls, **kwargs):
        try:
            if not cls.user_exists(kwargs['email']):
                user = User.objects.create_user(
                    kwargs['username'], kwargs['email'], kwargs['password'])
                user_profile = UserProfile.objects.create(
                    user=user, user_type=1)
                # redirect user to a differnt view
                return user_profile
            raise IntegrityError
        except IntegrityError:
            return None

    @classmethod
    def user_exists(cls, email):
        user = User.objects.filter(email=email)
        if user and user is not None:
            return True
        return False


class Member(models.Model):
    org_id = models.ForeignKey(UserProfile)
    user_id = models.IntegerField()
    user_level = models.PositiveSmallIntegerField(blank=False)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(UserProfile)
    project_name = models.CharField(blank=False, max_length=45)
    project_desc = models.CharField(blank=False, max_length=100)


class Team(models.Model):
    user_id = models.ForeignKey(UserProfile, related_name='users')
    project_id = models.ForeignKey(Project, related_name='projects')
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
