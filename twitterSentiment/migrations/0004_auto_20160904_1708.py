# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterSentiment', '0003_auto_20160904_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twittertext',
            name='twitter_user_id',
        ),
        migrations.AddField(
            model_name='twittertext',
            name='twitter_retweeted',
            field=models.BooleanField(default=False, verbose_name='retweeted'),
        ),
        migrations.AddField(
            model_name='twittertext',
            name='twitter_userid',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Twitter User ID'),
        ),
    ]
