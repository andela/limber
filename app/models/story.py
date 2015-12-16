from django.db import models

from .project import Project

class Story(models.Model):
    class Meta:
        app_label = 'app'

    story_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name="stories")
    name = models.CharField(blank=False, max_length=45)
    status = models.CharField(blank=False, max_length=45)
    category = models.CharField(blank=False, max_length=100)
    points = models.PositiveSmallIntegerField(blank=False)
    stage = models.CharField(max_length=100)


class Task(models.Model):
    class Meta:
        app_label = 'app'

    task_id = models.AutoField(primary_key=True)
    story = models.ForeignKey(Story)
    status = models.CharField(blank=False, max_length=45)
    description = models.CharField(max_length=255)