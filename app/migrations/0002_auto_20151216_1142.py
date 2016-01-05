# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='project',
            field=models.ForeignKey(related_name='stories', to='app.Project'),
        ),
    ]
