from django.db import models

from user import User

class Project(models.Model):
    class Meta:
    	app_label = 'app'

    project_id = models.IntegerField(primary_key=True)
    owner_id = models.ForeignKey(User)
    project_name = models.CharField(blank=False, max_length=45)
    project_desc = models.CharField(blank=False, max_length=100)


class Team(models.Model):
    class Meta:
        app_label = 'app'

    user_id = models.ForeignKey(User)
    project_id = models.ForeignKey(Project)
    user_level = models.PositiveSmallIntegerField(blank=False)