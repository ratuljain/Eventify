# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-18 09:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventify_api', '0011_auto_20170118_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventifyUser',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('user_profile_information', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='eventify_api.UserProfileInformation')),
                ('user_skills', models.ManyToManyField(
                    to='eventify_api.UserSkill')),
            ],
        ),
        migrations.RemoveField(
            model_name='eventify_user',
            name='user_profile_information',
        ),
        migrations.RemoveField(
            model_name='eventify_user',
            name='user_skills',
        ),
        migrations.AlterField(
            model_name='event',
            name='booking',
            field=models.ManyToManyField(
                through='eventify_api.UserEventBooking', to='eventify_api.EventifyUser'),
        ),
        migrations.AlterField(
            model_name='organiser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                       primary_key=True, serialize=False, to='eventify_api.EventifyUser'),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                       primary_key=True, serialize=False, to='eventify_api.EventifyUser'),
        ),
        migrations.AlterField(
            model_name='usereventbooking',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='eventify_api.EventifyUser'),
        ),
        migrations.DeleteModel(
            name='Eventify_User',
        ),
    ]
