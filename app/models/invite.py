import requests
import os
import hashlib

from random import random

from django.db import models
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives

from .project import Project
from .user import UserAuthentication
from app.invite_email import html_email


class ProjectInvite(models.Model):
	"""Project invite model."""
	email = models.EmailField(blank=False)
	invite_code = models.CharField(primary_key=True, max_length=100, blank=False)
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

	def send_invite_email(self):
		"""Method to send emails (containing project invite codes)
			to invitees through email.
		"""
		connection = mail.get_connection()

		# set the invite code to the ProjectInvite object
		self.invite_code = self.create_invite_code()

		host = os.environ.get('LIMBER_HOST')

		url = 'http://' + host + reverse('project-invites-list') + self.invite_code

		body = """Hi there!\n
				Welcome to Limber App. You have been invited to\n
				collaborate on project {}. To accept this invitation,\n
				click on the link below.\n\n\n
				{}
				\n\n\n
				If you have received this in error, please let us know.
				""".format(self.project.project_name, url)

		html_content = html_email.format(
			self.uid.profile.username,
			self.project.project_name,
			url
		)
		email = EmailMultiAlternatives(
			'Invitation to collaborate on project ' + self.project.project_name,
			body,
			self.uid.email,
			[self.email],
			connection=connection
		)
		email.attach_alternative(html_content, 'text/html')
		# send the email then save the invite to the database
		email.send()

	def create_invite_code(self):
		"""Create a hash to be sent as part of the URL to later identify the user
			when he/she responds to the invite.
		"""

		salt = random()
		nonlat = "{}4384834hhhhgsdhsdydsuyaisudhd {}".format(
			salt,
			self.email
		)
		string = nonlat.encode()
		i_code = hashlib.sha224(string).hexdigest()

		return i_code
