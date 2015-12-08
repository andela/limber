# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20151208_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_level', models.PositiveSmallIntegerField()),
                ('project', models.ForeignKey(related_name='members', to='app.Project')),
                ('user', models.ForeignKey(to='app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='project',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
