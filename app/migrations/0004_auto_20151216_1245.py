# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151216_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='attribute_name',
            new_name='stage',
        ),
        migrations.AlterField(
            model_name='story',
            name='project',
            field=models.ForeignKey(related_name='stories', to='app.Project'),
        ),
    ]
