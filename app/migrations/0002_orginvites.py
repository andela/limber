# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models.model_field_custom
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgInvites',
            fields=[
                ('email', app.models.model_field_custom.EmailFieldCaseInsensitive(max_length=254)),
                ('code', models.CharField(max_length=255, serialize=False, primary_key=True, blank=True)),
                ('accept', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Pending'), (1, b'Accepted'), (2, b'rejected')])),
                ('org', models.ForeignKey(related_name='invites', to='app.User')),
                ('uid', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
