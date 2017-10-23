# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 22:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0009_auto_20171020_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='book',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='bookreviews.Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='bookreviews.User'),
            preserve_default=False,
        ),
    ]
