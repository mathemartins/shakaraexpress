# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-09 19:23
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields
import services.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20180409_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='display_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=services.models.download_media_location),
        ),
    ]
