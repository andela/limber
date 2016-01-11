import os
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError, transaction
from .user import User, UserAuthentication
from . import model_field_custom
import hashlib
import random
from django.contrib.sites.models import Site
from django.conf.urls import url
from limber.settings import ALLOWED_HOSTS
class OrgInvites(models.Model):
	'''
		Model Handles pending invitations. and sends an email 
		to the invitee.
	'''
	Accepted_status = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'rejected')
    )
	email = model_field_custom.EmailFieldCaseInsensitive(unique=True)
	code = models.CharField(primary_key=True, max_length=255, blank=True)
	org = models.ForeignKey(User, related_name="invites")
	accept = models.PositiveSmallIntegerField(
	    blank=False, choices=Accepted_status, default=0)
	uid = models.ForeignKey(UserAuthentication)
	
    # Create hash code for the link

	def create_hash(self):
		# create hash 
		salt = hashlib.sha1(str(random.random())).hexdigest()[:1]
		email = self.email
		if isinstance(email, unicode):
			email = email.encode('utf-8')
		activation_key = hashlib.sha1(salt+email).hexdigest()
		return activation_key  

	def save(self, *args, **kwargs):
	# over ride the save() to include hash value before saving
	# check if invitee is already a member
	# check if the row with this hash already exists.
		import ipdb; ipdb.set_trace()
		if not self.pk:
			self.code = self.create_hash()
			self.send_email_notifictaion()
		super(OrgInvites, self).save(*args, **kwargs)

	def send_email_notifictaion(self):
		# Create Email notification
		#https://docs.djangoproject.com/en/dev/ref/contrib/sites/
		current_site = Site.objects.get_current().domain #Site.objects.get_current()
		link = ALLOWED_HOSTS[0]+'/api/orginvite/'+ self.code
		subject = 'Limber: Organisation invitations' 
		message = 'You been Invited to ' + self.org.username + \
				  ' organisation. Your activation code is '\
				  'http://'+ link 
		from_email = settings.EMAIL_HOST_USER
		to_list = [self.email, settings.EMAIL_HOST_USER]
		send_mail(subject, message, from_email, to_list, fail_silently=False)

	def email_is_member(self, email):
		user = member.objects.filter(email=email)
		if user:
			return True
		return user

