import os
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError, transaction
from rest_framework.response import Response
from .user import User, UserAuthentication, Member
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
	email = model_field_custom.EmailFieldCaseInsensitive(blank=False)
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
		
		if not self.pk:
			if self.send_email_notifictaion() == 1:

				self.code = self.create_hash()
			
				super(OrgInvites, self).save(*args, **kwargs)

	def send_email_notifictaion(self):
		
		# Create Email notification
		#https://docs.djangoproject.com/en/dev/ref/contrib/sites/
		current_site = Site.objects.get_current()
		link = '{0}/api/orginvite/{1}'.format( current_site, self.code)
		subject = 'Limber: Organisation invitations' 
		message = 'You been Invited to ' + self.org.username + \
				  ' organisation. Your activation code is '\
				  'http://'+ link 
		from_email = settings.EMAIL_HOST_USER
		to_list = [self.email]
		success = send_mail(subject, message, from_email, to_list, fail_silently=False)
		return success
	def email_is_member(self):
		
		#Check if emain belongs to a user
		userid = UserAuthentication.objects.filter(email=self.email)
		#check if user is a member of org
		user = Member.objects.filter(user=userid, org=self.org)
		if user:
			return True
		return Response(user)

