# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151216_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='project',
            field=models.ForeignKey(to='app.Project'),
        ),
    ]
