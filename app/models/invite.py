import requests
import os

from django.db import models

from .project import Project
from .user import UserAuthentication


class ProjectInvite(models.Model):
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

	@classmethod
	def send_invite_email(cls, request, **kwargs):
		"""Method to send emails containing project invite codes
			to invitees through email."""

		data = dict()
		data['from'] = request.user.email
		data['to'] = kwargs['email']
		data['subject'] = 'Invitation to collaborate on project ' +
		str(kwargs['project'].project_name)
		data['text'] = 'Welcome message. Also include an invite code within this.'

		response = requests.post(
			'https://api.mailgun.net/v3/mail.limberapp.xyz/messages',
			auth=('api', os.environ.get('MAILGUN_KEY')),
			data=data
		)
		return response
