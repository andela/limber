from django.db import models

from .user import User, UserAuthentication


class Project(models.Model):
    """Project Model."""

    project_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    project_name = models.CharField(blank=False, max_length=45)
    project_desc = models.CharField(blank=False, max_length=100)

    class Meta:
        app_label = 'app'

    def __str__(self):
        return self.project_name

    @classmethod
    def create_project(cls, **kwargs):
        """Custom method to add project."""
        if cls.check_project_exists(
                kwargs.get('owner'), kwargs.get('project_name')):
            return None
        else:
            project = Project.objects.create(
                owner=kwargs.get('owner'),
                project_name=kwargs.get('project_name'),
                project_desc=kwargs.get('project_desc')
            )
            if project:
                return project
        return None

    @classmethod
    def check_project_exists(cls, owner, project_name):
        """Check if user has a project by the given name."""
        project_exists = Project.objects.filter(
            owner=owner, project_name=project_name)
        if project_exists:
            return True
        return False


class TeamMember(models.Model):
    """Team member's model."""

    user = models.ForeignKey(UserAuthentication)
    project = models.ForeignKey(Project, related_name='team_members')
    user_level = models.PositiveSmallIntegerField(blank=False)

    class Meta:
        app_label = 'app'
