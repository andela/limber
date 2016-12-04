import os
import hashlib
from random import random

from django.db import models
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse

from app.html_emails.forgot_password_email import password_request_email
from .user import UserAuthentication


class PasswordReset(models.Model):
	"""Model to manage requests when user has 'forgotten password'."""

	reset_code = models.CharField(primary_key=True, max_length=100, blank=False)
	request_date = models.DateField(auto_now_add=True)
	request_completed = models.BooleanField(default=False)
	user = models.ForeignKey(UserAuthentication)

	def send_password_reset_email(self):
		"""Method to send password reset email."""
		connection = mail.get_connection()

		# set the reset code to the PasswordReset object
		self.reset_code = self.create_request_code()

		host = os.environ.get('LIMBER_HOST')

		url = 'http://' + host + '/password/reset/complete/' + self.reset_code

		body = """Hi there,\n
				Someone recently requested a password change for your\n
				Limber account. If this was you, you can set a new password <here>\n
				If you don't want to change your password or didn't request this,
				just ignore and delete this message.\n
				To keep your account secure, please don't forward this email to anyone.\n
				\n\n
				Thanks!
				- The Limber Team.
				"""

		html_content = password_request_email.format(
			url,
		)
		email = EmailMultiAlternatives(
			'Limber password reset',
			body,
			'helpdesk@limberapp.xyz',
			[self.user.email],
			connection=connection
		)
		email.attach_alternative(html_content, 'text/html')
		# send the email then save the invite to the database
		email.send()

	def create_request_code(self):
		"""
		Create a hash to be sent as part of the URL to later identify the user
		when he/she responds to the password reset request.
		"""

		salt = random()
		nonlat = "{0}4384834hhhhgsdhsdydsuyaisudhd {1}".format(
			salt,
			self.user.email
		)
		string = nonlat.encode()
		i_code = hashlib.sha224(string).hexdigest()

		return i_code

	def save(self, *args, **kwargs):
		"""
		Customize the save process to send password request email every time an
		instance of PasswordReset is saved.
		"""
		# if PasswordReset request hasn't been used before, send the reset email,
		# otherwise, just save
		if not self.request_completed:
			# send the email
			self.send_password_reset_email()
		# save to DB
		super(PasswordReset, self).save(*args, **kwargs)
