# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-01 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_booking_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
