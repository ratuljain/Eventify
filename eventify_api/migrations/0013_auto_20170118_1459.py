# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-18 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventify_api', '0012_auto_20170118_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventifyuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='eventifyuser',
            name='user_profile_information',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                       primary_key=True, serialize=False, to='eventify_api.UserProfileInformation'),
        ),
    ]
