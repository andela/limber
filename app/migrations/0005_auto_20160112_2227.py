# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models.model_field_custom


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151216_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=app.models.model_field_custom.CharFieldCaseInsensitive(unique=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='userauthentication',
            name='email',
            field=app.models.model_field_custom.EmailFieldCaseInsensitive(unique=True, max_length=254),
        ),
    ]
