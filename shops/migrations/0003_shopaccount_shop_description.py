# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-15 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_shopaccount_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopaccount',
            name='shop_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
