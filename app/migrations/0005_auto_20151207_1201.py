# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151202_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='owner_id',
        ),
        migrations.RemoveField(
            model_name='story',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='story_id',
        ),
        migrations.RemoveField(
            model_name='team',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Story',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
