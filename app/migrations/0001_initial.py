# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_level', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('project_name', models.CharField(max_length=45)),
                ('project_desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('story_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('status', models.CharField(max_length=45)),
                ('category', models.CharField(max_length=100)),
                ('points', models.PositiveSmallIntegerField()),
                ('attribute_name', models.CharField(max_length=100)),
                ('project_id', models.ForeignKey(to='app.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.IntegerField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=255)),
                ('story_id', models.ForeignKey(to='app.Story')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_level', models.PositiveSmallIntegerField()),
                ('project_id', models.ForeignKey(to='app.Project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=100)),
                ('login', models.CharField(max_length=45)),
                ('created_at', models.DateField(auto_now=True)),
                ('user_type', models.PositiveSmallIntegerField()),
                ('password', models.CharField(max_length=45)),
                ('city', models.CharField(max_length=70)),
                ('country', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='user_id',
            field=models.ForeignKey(to='app.User'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner_id',
            field=models.ForeignKey(to='app.User'),
        ),
        migrations.AddField(
            model_name='member',
            name='user_id',
            field=models.ForeignKey(to='app.User'),
        ),
    ]
