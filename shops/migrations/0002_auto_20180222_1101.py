# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-22 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopaccount',
            name='let_client_book_online',
            field=models.BooleanField(default=True),
        ),
    ]
