# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20151118_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.PositiveSmallIntegerField()),
                ('city', models.CharField(max_length=70)),
                ('country', models.CharField(max_length=45)),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='org_id',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner_id',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='team',
            name='user_id',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
