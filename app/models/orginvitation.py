import os
import requests
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
        salt = random.random()
        nonlat = "{}4384834hhhhgsdhsdydsuyaisudhd {}".format(salt, self.email)
        string = nonlat.encode()
        activation_key = hashlib.sha224(string).hexdigest()
        return activation_key

    def save(self, *args, **kwargs):
        # over ride the save() to include hash value before saving
        # check if invitee is already a member
        # check if the row with this hash already exists.

        if not self.pk:
            sent = self.send_email_notification()
            #if sent == 400:
            self.code = self.create_hash()
            super(OrgInvites, self).save(*args, **kwargs)

    def send_email_notification(self):

        # Create Email notification
        # https://docs.djangoproject.com/en/dev/ref/contrib/sites/
        current_site = Site.objects.get_current()
        link = '{0}/api/orginvite/{1}'.format(current_site, self.code)
        subject = 'Limber: Organisation invitations'
        message = 'You been Invited to ' + self.org.username + \
            ' organisation. Your activation code is '\
            'http://' + link
        from_email = settings.EMAIL_HOST_USER
        to_list = [self.email]
        # success = send_mail(
        #     subject, message, from_email, to_list, fail_silently=False)
        res = requests.post(
            "https://api.mailgun.net/v3/mail.limberapp.xyz/messages",
            auth=("api", "key-e9b5f771556874fa1fb09a55c343f8ce"),
            data={"from": from_email,
                  "to": to_list,
                  "subject": subject,
                  "text": message})
        return res
