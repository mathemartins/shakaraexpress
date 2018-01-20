# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-19 18:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0005_shopaccount_user_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=products.models.download_media_location)),
                ('title', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=500.0, max_digits=100, null=True)),
                ('sale_active', models.BooleanField(default=False)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, default=500.0, max_digits=100, null=True)),
                ('managers', models.ManyToManyField(blank=True, related_name='managers_products', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.ShopAccount')),
            ],
        ),
    ]
