# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20151207_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='owner_id',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='story',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='story_id',
            new_name='story',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='user_id',
            new_name='user',
        ),
    ]
