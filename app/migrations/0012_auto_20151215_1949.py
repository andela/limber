# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20151215_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
