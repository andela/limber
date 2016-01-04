from django.db import models

from .project import Project


class Story(models.Model):
    """Project story model."""

    story_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project)
    name = models.CharField(blank=False, max_length=45)
    status = models.CharField(blank=False, max_length=45)
    category = models.CharField(blank=False, max_length=100)
    points = models.PositiveSmallIntegerField(blank=False)
    attribute_name = models.CharField(max_length=100)

    class Meta:
        app_label = 'app'


class Task(models.Model):
    """Project tasks model."""

    task_id = models.AutoField(primary_key=True)
    story = models.ForeignKey(Story)
    status = models.CharField(blank=False, max_length=45)
    description = models.CharField(max_length=255)

    class Meta:
        app_label = 'app'
