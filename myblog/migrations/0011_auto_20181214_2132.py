# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0010_auto_20181214_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to='upload/'),
        ),
    ]