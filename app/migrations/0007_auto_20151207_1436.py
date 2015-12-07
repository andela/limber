# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_project_story_task_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
