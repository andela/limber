from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    user_name = models.CharField(blank=False, max_length=45)
    created_at = models.DateField(auto_now=True)
    user_type = models.PositiveSmallIntegerField(blank=False)
    password = models.CharField(max_length=45)
    city = models.CharField(max_length=70)
    country = models.CharField(max_length=45)

    def usernames(self):
        return '{0}{1}'.format(self.user_name, self.email)


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
