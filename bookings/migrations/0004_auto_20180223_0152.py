# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-23 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20180223_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='mobile_number',
            field=models.IntegerField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]