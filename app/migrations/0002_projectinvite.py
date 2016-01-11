# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInvite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('invite_code', models.CharField(max_length=100)),
                ('accept', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Pending'), (1, b'Accepted'), (2, b'Rejected')])),
                ('project', models.ForeignKey(to='app.Project')),
                ('uid', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
