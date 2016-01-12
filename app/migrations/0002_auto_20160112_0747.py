# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models.model_field_custom


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orginvites',
            name='email',
            field=app.models.model_field_custom.EmailFieldCaseInsensitive(max_length=254),
        ),
    ]
