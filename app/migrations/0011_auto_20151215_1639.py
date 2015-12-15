# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20151208_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='project',
            field=models.ForeignKey(related_name='team_members', to='app.Project'),
        ),
    ]
