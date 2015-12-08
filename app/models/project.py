from django.db import models

from .user import User

class Project(models.Model):

    class Meta:
    	app_label = 'app'

    project_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    project_name = models.CharField(blank=False, max_length=45)
    project_desc = models.CharField(blank=False, max_length=100)



class TeamMember(models.Model):

    class Meta:
        app_label = 'app'

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, related_name='team_members')
    user_level = models.PositiveSmallIntegerField(blank=False)