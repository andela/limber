# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuthentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=70, blank=True)),
                ('last_name', models.CharField(max_length=70, blank=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('user_level', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(serialize=False, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=70)),
                ('name', models.CharField(unique=True, max_length=90, blank=True)),
                ('user_type', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
            name='org_id',
            field=models.ForeignKey(to='app.User'),
        ),
        migrations.AddField(
            model_name='userauthentication',
            name='profile_id',
            field=models.ForeignKey(related_name='pro', to='app.User'),
        ),
    ]
