# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='login',
            new_name='user_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
