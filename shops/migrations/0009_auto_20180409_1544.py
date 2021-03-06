# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-09 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0008_shopaccount_working_hours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopaccount',
            options={'ordering': ['-timestamp', '-updated']},
        ),
        migrations.AddField(
            model_name='shopaccount',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shopaccount',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
