# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-17 13:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventify_api', '0004_auto_20170117_1331'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='Eventify_User',
        ),
        migrations.RenameModel(
            old_name='UserSkills',
            new_name='UserSkill',
        ),
    ]
