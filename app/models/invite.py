from django.db import models
from .project import Project
from .user import UserAuthentication


class ProjectInvites(models.Model):
	"""Project invite model."""
	id = models.AutoField(primary_key=True)
	email = models.EmailField(blank=False)
	invite_code = models.CharField(blank=False, max_length=100)
	project = models.ForeignKey(Project)

	PENDING = 0
	ACCEPTED = 1
	REJECTED = 2
	ACCEPT_CHOICES = (
		(PENDING, 'Pending'),
		(ACCEPTED, 'Accepted'),
		(REJECTED, 'Rejected'),
	)
	accept = models.PositiveSmallIntegerField(
		choices=ACCEPT_CHOICES,
		default=PENDING
	)
	uid = models.ForeignKey(UserAuthentication)
