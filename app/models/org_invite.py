import requests
from django.conf import settings
from django.db import models
from .user import User, UserAuthentication
from . import model_field_custom
import hashlib
import random
from django.contrib.sites.models import Site
from app.invite_email import html_email
import socket



class OrgInvites(models.Model):
    '''
            Model Handles pending invitations. and sends an email
            to the invitee.
    '''

    ACCEPTED_STATUS = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'rejected')
    )
    email = model_field_custom.EmailFieldCaseInsensitive(blank=False)
    code = models.CharField(primary_key=True, max_length=255, blank=True)
    org = models.ForeignKey(User, related_name="invites")
    accept = models.PositiveSmallIntegerField(
        blank=False, choices=ACCEPTED_STATUS, default=0)
    uid = models.ForeignKey(UserAuthentication)

    # Create hash code for the link
    def create_hash(self):
        # create hash
        salt = random.random()
        nonlat = "{0}4384834hhhhgsdhsdydsuyaisudhd {1}".format(
            salt, self.email)
        string = nonlat.encode()
        activation_key = hashlib.sha224(string).hexdigest()
        return activation_key

    def save(self, *args, **kwargs):
        # over ride the save() to include hash value before saving
        # check if invitee is already a member,
        # check if the row with this hash already exists.
       
        if not self.pk:
            self.code = self.create_hash()
            self.send_email_notification()
            super(OrgInvites, self).save(*args, **kwargs)

    def send_email_notification(self):
        # Create Email notification
        # https://docs.djangoproject.com/en/dev/ref/contrib/sites/
        current_site = socket.gethostname()
        link = '{0}/confirm/?code={1}'.format(current_site, self.code)
        subject = 'Limber: Organisation invitations'
        message = html_email.format(
            self.uid.profile.username,
            self.org,
            link,
            "Organisation")
        from_email = settings.EMAIL_HOST_USER
        to_list = [self.email]
        response = requests.post(
            "https://api.mailgun.net/v3/mail.limberapp.xyz/messages",
            auth=("api", "key-e9b5f771556874fa1fb09a55c343f8ce"),
            data={"from": from_email,
                  "to": to_list,
                  "subject": subject,
                  "text": message})
        return response
